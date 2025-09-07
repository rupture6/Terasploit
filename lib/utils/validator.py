# -*- coding: utf-8 -*-

# Python library
import re
from typing import Any
from pathlib import Path

# Library
from lib.utils.printer import printf

# Precompiled Regex Patterns

UNICODE_RANGE = r"\u00a1-\uffff"

IPV4_PATTERN = (
    r"(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)"
    r"(?:\.(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)){3}"
)
IPV6_PATTERN = r"\[[0-9a-f:.]+\]"

HOSTNAME = (
    rf"[a-z{UNICODE_RANGE}0-9]"
    rf"(?:[a-z{UNICODE_RANGE}0-9-]{{0,61}}[a-z{UNICODE_RANGE}0-9])?"
)
DOMAIN = rf"(?:\.(?!-)[a-z{UNICODE_RANGE}0-9-]{{1,63}}(?<!-))*"
TLD = (
    rf"\.(?!-)(?:[a-z{UNICODE_RANGE}-]{{2,63}}"
    r"|xn--[a-z0-9]{1,59})(?<!-)\.?"
)
HOST_PATTERN = rf"({HOSTNAME}{DOMAIN}{TLD}|localhost)"

URL_REGEX = re.compile(
    rf"^(?:http|ftp)s?://"
    rf"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"
    rf"(?:{IPV4_PATTERN}|{IPV6_PATTERN}|{HOST_PATTERN})"
    rf"(?::[0-9]{{1,5}})?"
    rf"(?:[/?#][^\s]*)?$",
    re.IGNORECASE,
)

IPV4_REGEX = re.compile(
    r"(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])"
    r"(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])",
    re.IGNORECASE,
)

IPV6_REGEX = re.compile(
    r"^(([0-9a-f]{1,4}:){7,7}[0-9a-f]{1,4}"
    r"|([0-9a-f]{1,4}:){1,7}:"
    r"|([0-9a-f]{1,4}:){1,6}:[0-9a-f]{1,4}"
    r"|([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}"
    r"|([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}"
    r"|([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}"
    r"|([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}"
    r"|[0-9a-f]{1,4}:((:[0-9a-f]{1,4}){1,6})"
    r"|:((:[0-9a-f]{1,4}){1,7}|:)"
    r"|fe80:(:[0-9a-f]{0,4}){0,4}%[0-9a-z]{1,}"
    r"|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?\d)?\d)\.){3,3}"
    r"(25[0-5]|(2[0-4]|1?\d)?\d)"
    r"|([0-9a-f]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?\d)?\d)\.){3,3}"
    r"(25[0-5]|(2[0-4]|1?\d)?\d))$",
    re.IGNORECASE,
)


class Validate:
    """ Validates module options """

    @staticmethod
    def url(value: str) -> bool:
        """ Validate a URL/URI string """
        return bool(URL_REGEX.fullmatch(value))

    @staticmethod
    def ipaddress(value: str) -> bool:
        """ Validate IPv4 or IPv6 address """
        return bool(IPV4_REGEX.fullmatch(value) or IPV6_REGEX.fullmatch(value))

    @staticmethod
    def host(value: str) -> bool:
        """ Validate host (IP address or URL) """
        return Validate.ipaddress(value) or Validate.url(value)

    @staticmethod
    def int_object(value: Any) -> bool:
        """ Check if value can be interpreted as int """
        if isinstance(value, int):
            return True
        return isinstance(value, str) and value.isdigit()

    @staticmethod
    def float_object(value: Any) -> bool:
        """ Check if value can be interpreted as float """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def int_float_object(value: Any) -> bool:
        """ Check if value is int or float-like """
        return Validate.int_object(value) or Validate.float_object(value)

    @staticmethod
    def string_object(value: Any) -> bool:
        """ Check if value is a string """
        return isinstance(value, str)

    @staticmethod
    def boolean(value: Any) -> bool:
        """ Check if value is a boolean or 'true'/'false' string """
        if isinstance(value, bool):
            return True
        if isinstance(value, str):
            return value.lower() in {"true", "false"}
        return False

    @staticmethod
    def port(value: Any) -> bool:
        """ Validate TCP/UDP port number (1-65535) """
        if isinstance(value, int):
            return 1 <= value <= 65535
        if isinstance(value, str) and value.isdigit():
            return 1 <= int(value) <= 65535
        return False

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """ Check if a file exists """
        try:
            return Path(file_path).is_file()
        except OSError as err:
            printf(f"error => {err}")
            return False
