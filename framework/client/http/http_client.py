# -*- coding: utf-8 -*-

# Python3
import requests
import urllib3
from typing import Any
from requests.auth import HTTPDigestAuth

# Library
from lib.utils.exception import InvalidError

# Framework
from framework.console.options import OptGet

# List of http methods
http_methods = ["get", "post", "put", "delete", "head", "options", "patch"]

# Disable insecure request warning because it doesn't help at all
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HTTP:
    """ HTTP client session """

    session = requests.Session()

    @classmethod
    def reset_session(cls) -> None:
        """ Reset the current session via closing and creating a new one """

        # Close the current existing session
        cls.http_session.close()

        # Create a new session
        cls.http_session = requests.Session()


def _format_request_content(kwargs: dict[str, Any]) -> dict[str, Any]:
    """ Format the request content """
    request_content: dict[str, Any] = {}

    # Formats the value of request content
    for key, value in kwargs.items():
        try:
            # formats to float only
            request_content[key] = float(str(value))
        except (TypeError, ValueError):
            request_content[key] = value

    # Return the formatted request content
    return request_content


def http_request(
    method: str,
    url: str | None = None,
    params: dict[Any, Any] = {},
    data: dict[Any, Any] = {},
    headers: dict[Any, Any] = {},
    cookies: dict[Any, Any] = {},
    files: dict[Any, Any] = {},
    auth: tuple[str, str] | None = None,
    timeout: int | float | None = None,
    cert: str | tuple[Any] | None = None,
    stream: bool | None = None,
    json: dict[Any, Any] = {},
    proxies: dict[Any, Any] = OptGet("PROXY"),
    verify: bool = OptGet("SSL"),
    auth_type: str = "BASIC"
) -> requests.Response:
    """ Perform an HTTP request """

    # Check if method is correct
    if not method.lower() in http_methods:
        raise InvalidError(f"Invalid HTTP method: {method}")

    # Formats the requests contents
    requests_contents = _format_request_content(
        {
            "url": url,
            "params": params,
            "data": data,
            "headers": headers,
            "cookies": cookies,
            "files": files,
            "timeout": timeout,
            "proxies": proxies,
            "verify": verify,
            "cert": cert,
            "stream": stream,
            "json": json,
        }
    )
    if auth:
        if auth_type.upper() == "BASIC":
            requests_contents["auth"] = auth
        if auth_type.upper() == "DIGEST":
            requests_contents["auth"] = HTTPDigestAuth(auth[0], auth[1])
        if auth_type.upper() not in ("DIGEST", "BASIC"):
            raise TypeError(f"Authentication type is invalid... {auth_type}")
    else:
        requests_contents["auth"] = None

    # Get the request method attribute
    request_lib = getattr(requests, method.lower())

    # Perform the http request via executing requests library
    response = request_lib(**requests_contents)

    # Return the http request response
    return response
