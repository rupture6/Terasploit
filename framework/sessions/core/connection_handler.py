# -*- coding: utf-8 -*-

# Python library
import socket
import threading
import time
import select

# Library
from lib.container.module import Module
from lib.utils.printer import print_status, print_error
from lib.socks.check_host import is_ipv4, is_ipv6

# Framework
from framework.client.tcp.tcp_client import TCPClient
from framework.sessions.core.thread_handler import Session


def handle_connection(
    client_socket: socket.socket,
    client_address: str,
    port: int
) -> None:
    """ Handle client connection lifecycle """
    try:
        while not Session.alive.is_set():
            if client_socket.fileno() == -1:
                print_error(
                    f"Socket closed or invalid += {client_address}:{port}"
                )
                break

            readable, _, error = select.select(
                [client_socket], [], [client_socket], 5
            )
            if error:
                break

            if readable:
                try:
                    # Peek data without consuming it
                    data = client_socket.recv(1, socket.MSG_PEEK)
                    if not data:
                        print_error(
                            f"Disconnected += {client_address}:{port}"
                        )
                        break
                except BlockingIOError:
                    continue

    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
        print_error(f"Connection is broken += {client_address}:{port}")

    except socket.error:
        pass

    finally:
        try:
            print_status(f"Connection closed += {client_address}:{port}")
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

            with Session.thread_lock:
                Session.sessions = [
                    sess for sess in Session.sessions
                    if sess[1] != (client_address, port)
                ]
        except OSError:
            with Session.thread_lock:
                Session.sessions = [
                    sess for sess in Session.sessions
                    if sess[1] != (client_address, port)
                ]


class ReverseTCPHandler:
    """ Reverse TCP exploit handler """

    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port

        Session.server_socket = self.get_socket()
        print_status(
            f"Started reverse TCP handler on {self.host}:{self.port}"
        )

    def get_socket(self) -> socket.socket:
        """ Create a socket object based on the host """
        sock: socket.socket | None = None

        if is_ipv4(self.host):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if is_ipv6(self.host):
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        if not sock:
            raise ValueError("Failed to create socket, invalid host.")

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def start_handler(self) -> None:
        """ Bind and listen for client connections """
        try:
            Session.server_socket.bind((self.host, self.port))
        except OSError as err:
            Session.server_socket.close()
            if err.errno == 99:
                print_error(
                    f"Cannot assign requested address "
                    f"{self.host}:{self.port}."
                )
            else:
                print_error(
                    f"Failed to bind to {self.host}:{self.port}."
                )
            return

        Session.server_socket.listen(5)
        print_status(f"Listening on {self.host}:{self.port}...")

        while not Session.active_listener.is_set():
            try:
                client_socket, client_address = (
                    Session.server_socket.accept()
                )
                print_status(
                    f"Connection accepted += "
                    f"{client_address[0]}:{client_address[1]}"
                )
                conn_handler = threading.Thread(
                    target=handle_connection,
                    args=(client_socket, client_address[0], client_address[1]),
                    daemon=True
                )
                conn_handler.start()

                client_socket.setblocking(False)
                with Session.thread_lock:
                    Session.sessions.append((
                        client_socket,
                        client_address,
                        Module.module.info["Name"],
                        "reverse_tcp",
                        conn_handler
                    ))

            except socket.timeout:
                pass
            except OSError:
                print_status("Listener stopped.")


class BindTCPHandler:
    """ Bind TCP exploit handler """

    def __init__(self, rhost: str, lport: int) -> None:
        self.rhost: str = rhost
        self.lport: int = lport
        self.client_socket: socket.socket = TCPClient.create_socket(rhost)
        self.set_sock_opts()

        print_status(f"Started bind TCP handler on {rhost}:{lport}")

    def set_sock_opts(self) -> None:
        """ Set socket options to keep the TCP connection alive """
        self.client_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_KEEPALIVE,
            1
        )
        self.client_socket.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPIDLE,
            1
        )
        self.client_socket.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPINTVL,
            1
        )
        self.client_socket.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPCNT,
            5
        )

    def start_handler(self) -> None:
        """ Connect to the server and manage the session """
        print_status(f"Connecting to {self.rhost}:{self.lport}...")
        while not Session.active_connector.is_set():

            # Prevent rapid reconnection attempts
            time.sleep(1)
            try:
                TCPClient.connect(self.client_socket, self.rhost, self.lport)
                print_status(f"Connected to {self.rhost}:{self.lport}")

                conn_handler = threading.Thread(
                    target=handle_connection,
                    args=(self.client_socket, self.rhost, self.lport),
                    daemon=True
                )
                conn_handler.start()

                with Session.thread_lock:
                    Session.sessions.append((
                        self.client_socket,
                        (self.rhost, self.lport),
                        Module.module.info["Name"],
                        "bind_tcp",
                        conn_handler
                    ))

            except (ConnectionError, socket.error):
                pass
