# -*- coding: utf-8 -*-

# Python3
import requests
import urllib3
from typing import Any

# Library
from lib.utils.exception import InvalidError

# Disable insecure request warning because it doesn't help at all
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# List of http methods
http_methods = [
    "get",
    "post",
    "put",
    "delete",
    "head",
    "options",
    "patch"
]


class HTTP:
    """ HTTP session """

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
            request_content[key] = float(value)
        except ValueError:
            request_content[key] = value

    # Return the formatted request content
    return request_content


def http_request(
    method: str,
    url: str | None = None,
    params: dict[Any, Any] | None = None,
    data: dict[Any, Any] | None = None,
    headers: dict[Any, Any] | None = None,
    cookies: dict[Any, Any] | None = None,
    files: dict[Any, Any] | None = None,
    auth: tuple[Any] | None = None,
    timeout: int | float | None = None,
    proxies: dict[Any, Any] | None = None,
    verify: bool | None = None,
    cert: str | tuple[Any] | None = None,
    stream: bool | None = None,
    json: dict[Any, Any] | None = None,
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
            "auth": auth,
            "timeout": timeout,
            "proxies": proxies,
            "verify": verify,
            "cert": cert,
            "stream": stream,
            "json": json,
        }
    )

    # Get the request method attribute
    request_lib = getattr(requests, method.lower())

    # Perform the http request via executing requests library
    response = request_lib(**requests_contents)

    # Return the http request response
    return response
