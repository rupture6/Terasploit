# -*- coding: utf-8 -*-

# Python library
import socket

# Library
from lib.socks.check_host import is_ipv4, is_ipv6


class UDPClient:
    """ UDP socket client for establishing and managing a UDP connection """

    @staticmethod
    def create_socket(host: str) -> socket.socket:
        """Create a socket object based on the host type (IPv4 or IPv6)."""
        if is_ipv4(host):
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if is_ipv6(host):
            return socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        raise ValueError(
            f"Invalid host '{host}': must be IPv4 or IPv6 address."
        )

    @staticmethod
    def connect(sock: socket.socket, host: str, port: int) -> socket.socket:
        """ Connect to the server """
        sock.connect((host, port))
        return sock
