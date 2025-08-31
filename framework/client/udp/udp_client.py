# -*- coding: utf-8 -*-

# Python lib
import socket

# Lib
from lib.socks.check_host import is_ipv4, is_ipv6


class UDPClient:
    """UDP socket client for establishing and managing a UDP connection."""

    def __init__(self, host: str, port: int) -> None:
        """Initialize the UDP client."""
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None

    def _create_socket(self) -> socket.socket:
        """Create a socket object based on the host type (IPv4 or IPv6)."""
        if is_ipv4(self.host):
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if is_ipv6(self.host):
            return socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        raise ValueError(
            f"Invalid host '{self.host}': must be IPv4 or IPv6 address."
        )

    def connect(self) -> socket.socket:
        """Connect to the server."""
        self.sock = self._create_socket()
        self.sock.connect((self.host, self.port))
        return self.sock

    def close(self) -> None:
        """Close the socket connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
