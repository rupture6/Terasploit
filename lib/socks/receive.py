# -*- coding: utf-8 -*-

# Python library
import socket
import select

# Library
from lib.utils.printer import print_error

# Framework
from framework.console.options import Opt


def socket_receive(
    client_socket: socket.socket,
    buffer_size: int = 4096,
    timeout: int = 1
) -> bytes:
    """ Receive data from a socket until it is closed or a timeout occurs """
    received_data = b""

    while True:
        try:
            readable, _, _ = select.select([client_socket], [], [], timeout)
            if not readable:
                break

            chunk = client_socket.recv(buffer_size)
            if not chunk:
                break
            received_data += chunk

        except socket.error as err:
            print_error(err, verbose=Opt.options["VERBOSE"])
            break

    return received_data


def receive_fixed_size_data(
    client_socket: socket.socket,
    expected_size: int,
    buffer_size: int = 4096,
    timeout: int = 1
) -> bytes:
    """ Receive a fixed amount of data from a socket until it is closed """
    received_data = b""

    while len(received_data) < expected_size:
        try:
            readable, _, _ = select.select([client_socket], [], [], timeout)
            if not readable:
                break

            chunk = client_socket.recv(
                min(
                    expected_size - len(received_data),
                    buffer_size
                )
            )
            if not chunk:
                break
            received_data += chunk

        except socket.error as err:
            print_error(err, verbose=Opt.options["VERBOSE"])
            break

    return received_data
