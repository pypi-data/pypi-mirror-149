import json
from dataclasses import asdict, dataclass, field
from json import JSONDecodeError
from typing import Any

import pydash
import requests

from mb_std import md

FIREFOX_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0"
CHROME_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"  # noqa


@dataclass
class HResponse:
    """HTTP Response"""

    http_code: int = 0
    error: str | None = None
    body: str = ""
    headers: dict = field(default_factory=lambda: {})

    _json_data: dict = field(default_factory=lambda: {})
    _json_parsed = False
    _json_parsed_error = False

    def _parse_json(self):
        try:
            self._json_data = {}
            self._json_data = json.loads(self.body)
            self._json_parsed_error = False
        except JSONDecodeError:
            self._json_parsed_error = True
        self._json_parsed = True

    @property
    def json(self) -> Any:
        if not self._json_parsed:
            self._parse_json()
        return self._json_data

    @property
    def json_parse_error(self) -> bool:
        if not self._json_parsed:
            self._parse_json()
        return self._json_parsed_error

    def to_error(self, error=None):
        from mb_std import Result

        return Result(error=error if error else self.error, data=asdict(self))

    def to_ok(self, result: Any):
        from mb_std import Result

        return Result(ok=result, data=asdict(self))

    def is_error(self):
        return self.error is not None

    def is_timeout_error(self):
        return self.error == "timeout"

    def is_proxy_error(self):
        return self.error == "proxy_error"

    def is_connection_error(self):
        return self.error and self.error.startswith("connection_error:")

    def to_dict(self):
        return pydash.omit(asdict(self), "_json_data")


def http_request(
    url: str,
    *,
    method="GET",
    proxy: str | None = None,
    params: dict | None = None,
    headers: dict | None = None,
    cookies: dict | None = None,
    timeout: int = 10,
    user_agent: str | None = None,
    json_params: bool = True,
    auth=None,
) -> HResponse:
    method = method.upper()
    proxies = {"http": proxy, "https": proxy} if proxy else None
    if not headers:
        headers = {}
    try:
        headers["user-agent"] = user_agent
        request_params = md(method, url, proxies, timeout, headers, cookies, auth)
        if method == "GET":
            request_params["params"] = params
        elif json_params:
            request_params["json"] = params
        else:
            request_params["data"] = params
        r = requests.request(**request_params)
        return HResponse(http_code=r.status_code, body=r.text, headers=dict(r.headers))
    except requests.exceptions.Timeout:
        return HResponse(error="timeout")
    except requests.exceptions.ProxyError:
        return HResponse(error="proxy_error")
    except requests.exceptions.ConnectionError as e:
        return HResponse(error=f"connection_error: {str(e)}")
    except Exception as err:
        return HResponse(error=f"exception: {str(err)}")


hr = http_request
