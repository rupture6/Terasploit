# -*- coding: utf-8 -*-
"""
Session: Generic pulsar session
Description:
    This session does not have any special functionality.
    It only starts an interactive shell to send commands to the target.
"""

import socket

from lib.socks.receive import socket_receive
from lib.utils.printer import (
    printf,
    print_error,
    print_status
)

WELCOME = """
Welcome to pulsar interactive shell.

NOTE:
  This is a generic pulsar session, it does not have any special functionality.
  You can only execute system commands from the target.
"""


def session(client_socket: socket.socket):
    """ Interactive pulsar `generic` shell """

    # Print the welcome message
    printf(WELCOME)

    # The prompt of the shell
    prompt = "\001\x1b[4m\002pulsar\001\x1b[0m\002 > "

    # Keep the session active
    active = True

    while active:
        try:
            command = input(prompt).strip()
            if command in ("exit", "background", "pause", "close"):
                active = False
                print_status("Putting session in background.")
                continue

            # Add a new line to the command
            command += "\n"

            # Send the command to the target
            client_socket.send(command.encode())

            # Receive and print the output
            output = socket_receive(client_socket)
            printf(output.decode("utf-8"))

        except KeyboardInterrupt:
            printf("CTRL+C signal... use command background to quit session.")

        except socket.error as error:
            print_error(error)
            active = False
