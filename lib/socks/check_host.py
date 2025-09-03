# -*- coding: utf-8 -*-

# Python library
import ipaddress


def is_ipv4(ip: str) -> bool:
    """ Check if a string is a valid IPv4 address """
    try:
        return isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)
    except ValueError:
        return False


def is_ipv6(ip: str) -> bool:
    """ Check if a string is a valid IPv6 address """
    try:
        return isinstance(ipaddress.ip_address(ip), ipaddress.IPv6Address)
    except ValueError:
        return False
