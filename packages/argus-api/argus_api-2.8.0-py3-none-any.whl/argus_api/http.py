import os

from typing import Optional, List, Union

from requests import Response
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


from argus_api._validators import validate_http_response

try:
    from argus_cli.settings import settings
except ImportError:
    settings = {}

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, timeout=30, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


package_version = version("argus-api")


class ArgusAPISession:

    SUPPORTED_METHODS = ("get", "post", "put", "delete")
    USER_AGENT = f"ArgusAPI/{package_version}"
    DEFAULT_TIMEOUT = 30  # seconds
    TIMEOUT_ENV_VAR = "ARGUS_API_TIMEOUT"
    # retry strategy defaults
    DEFAULT_RETRY_MAX = 3
    DEFAULT_RETRY_STATUSES = [500, 503, 504]
    DEFAULT_RETRY_METHODS = ["GET", "PUT", "DELETE", "POST"]
    # Used to calculate sleep time between retries. backoff sleep time formula:
    # {backoff factor} * (2 ** ({number of total retries} - 1))
    DEFAULT_RETRY_BACKOFF_FACTOR = 0

    # instance attributes

    #: API key used to authenticate requests.
    api_key: str
    #: API base URL. Should not contain a trailing ``/``.
    base_url: str
    #: proxies dictionary as expected by the ``proxies`` argument of
    #: :func:`requests.request`
    proxies: dict
    #: SSL certify verification setting as expected by the ``verify`` argument
    #: of :func:`requests.request`
    verify: Union[bool, str]

    def __init__(self):
        self.user_agent = self.USER_AGENT
        self.api_key = settings.get("api", {}).get("api_key")
        self.base_url = settings.get("api", {}).get(
            "api_url", "https://api.mnemonic.no"
        )

        self._session = Session()
        # set default timeout and retry strategy
        self.default_timeout = int(
            os.getenv(
                self.TIMEOUT_ENV_VAR,
                settings.get("api", {}).get("timeout", self.DEFAULT_TIMEOUT),
            )
        )
        self.max_retries = self.DEFAULT_RETRY_MAX
        self.retry_statuses = self.DEFAULT_RETRY_STATUSES
        self.retry_methods = self.DEFAULT_RETRY_METHODS
        self.backoff_factor = self.DEFAULT_RETRY_BACKOFF_FACTOR

        self.set_adapter()
        # set headers
        self._session.headers.update(
            {"User-Agent": self.USER_AGENT, "content": "application/json"}
        )
        if self.api_key:
            self._session.headers.update({"Argus-API-Key": self.api_key})

        self._verify = None

    @property
    def proxies(self):
        return self._session.proxies

    @proxies.setter
    def proxies(self, value):
        self._session.proxies = value

    @property
    def verify(self):
        return self._session.verify

    @verify.setter
    def verify(self, value):
        self._verify = value
        self._session.verify = value

    def set_timeout(self, timeout: int):
        """Sets the default timeout for the session

        :param timeout: new default timeout in seconds
        """
        self.set_adapter(default_timeout=timeout)

    def set_adapter(
        self,
        default_timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_statuses: Optional[List[int]] = None,
        retry_methods: Optional[List[str]] = None,
        backoff_factor: Optional[int] = None,
    ):
        """Sets the HTTP adapter for the session

        this controls global timeout and retry settings.

        :param default_timeout: default timeout in seconds
        :param max_retries: maximun retries on failures
        :param retry_statuses: HTTP status codes on which to retry
        :param retry_methods: whitelist of methods for which retries will be performed
        :param backoff_factor: factor for incremental retry delays
        """
        self.default_timeout = default_timeout or self.default_timeout
        self.max_retries = max_retries or self.max_retries
        self.retry_statuses = retry_statuses or self.retry_statuses
        self.retry_methods = retry_methods or self.retry_methods
        self.backoff_factor = backoff_factor or self.backoff_factor

        self.retry_strategy = Retry(
            total=self.max_retries,
            status_forcelist=self.retry_statuses,
            method_whitelist=self.retry_methods,
            raise_on_redirect=False,
            backoff_factor=self.backoff_factor,
            raise_on_status=False,
        )
        adapter = TimeoutHTTPAdapter(
            timeout=self.default_timeout, max_retries=self.retry_strategy
        )
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def _request(self, method, _route, *args, **kwargs) -> Response:
        """

        _route should have a leading /
        """

        # build destination URL
        base_url = self.base_url
        if kwargs.get("server_url"):
            base_url = kwargs["server_url"]
        url = f"{base_url}{_route}"

        # allow auth header override
        api_settings = settings.get("api", {})
        headers_override = {}
        if kwargs.get("apiKey"):
            headers_override["Argus-Api-Key"] = kwargs["apiKey"]
        elif kwargs.get("authentication"):
            authentication = kwargs["authentication"]
            if isinstance(authentication, dict):
                headers_override["Argus-Api-Key"] = None
                headers_override.update(authentication)
            elif callable(authentication):
                headers_override["Argus-Api-Key"] = None
                headers_override.update(authentication(url))

        else:
            # settings are changed at runtime, we need to re-check them
            api_key = api_settings.get("api_key", self.api_key)
            headers_override["Argus-Api-Key"] = api_key
        timeout = int(
            os.getenv(
                self.TIMEOUT_ENV_VAR,
                api_settings.get("timeout", self.default_timeout),
            )
        )
        if "timeout" not in kwargs and timeout != self.default_timeout:
            kwargs["timeout"] = timeout

        # update request-specific headers
        if headers_override:
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"].update(headers_override)

        # the following "verify" logic is convoluted in an effort to preserve backward
        # compatibility
        # TODO: clean up for next major bump
        if self._verify is not None:
            # if _verify is set, we can let user-defined parameter take precedence
            # over the environment without breaking backward compatibility
            if kwargs.get("verify") is not None:
                kwargs["verify"] = kwargs.get("verify", self._verify)
            else:
                kwargs["verify"] = self._verify
        else:
            # otherwise, emulate previous behavior where the verify parameter
            # would be ignored if a CA bundle is defined in order to maintain backward
            # compatibility.
            # we also need to convert verify=None to True to stay compatible with the
            # previous "True" default.
            kwargs_verify = True if kwargs.get("verify") is None else kwargs["verify"]
            kwargs["verify"] = os.getenv(
                "REQUESTS_CA_BUNDLE",
                os.getenv("CURL_CA_BUNDLE", kwargs_verify),
            )

        # remove proxies from the args if not set to avoid overriding the
        # session-level proxies
        if "proxies" in kwargs and kwargs["proxies"] is None:
            del kwargs["proxies"]

        # clean kwargs before passing them down to requests
        for arg in ("apiKey", "authentication", "server_url"):
            if arg in kwargs:
                del kwargs[arg]

        # perform the request
        response = getattr(self._session, method)(url, *args, **kwargs)

        # check the status code for errors
        validate_http_response(response)

        return response

    def get(self, _route, *args, **kwargs):
        return self._request("get", _route, *args, **kwargs)

    def post(self, _route, *args, **kwargs):
        return self._request("post", _route, *args, **kwargs)

    def put(self, _route, *args, **kwargs):
        return self._request("put", _route, *args, **kwargs)

    def delete(self, _route, *args, **kwargs):
        return self._request("delete", _route, *args, **kwargs)


session = ArgusAPISession()
