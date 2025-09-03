# -*- coding: utf-8 -*-

# Python library
import subprocess
import os
import shlex
import readline
import atexit
import traceback
from typing import Any

# Library
from lib.container.module import Module
from lib.container.console import ConsoleSettings, LogManager
from lib.utils.exception import TerasploitException, InvalidError
from lib.utils.printer import (
    print_status,
    print_warning,
    print_error,
    printf
)

# Framework
from framework.console.banner import display_banner
from framework.console.logs import Log
from framework.sessions.thread_handler import Session
from framework.console.command.core import Command


class Interpreter(Command):
    """The main interpreter class."""

    # Activates and deactivates the command line interface
    activate_command_line: bool = False

    # History file and length
    history_length: int = 100
    history_file: str = os.path.join(
        os.path.expanduser("~"),
        ".tera_history"
    )

    # Termination commands
    terminate_command = ["exit", "quit", "done", "close", "terminate"]

    def __init__(self) -> None:
        """ Initialize the interpreter """

        # Initialize logging
        LogManager.instance = Log(
            logfile="terasploit.log",
            level=ConsoleSettings.log_level,
            console=ConsoleSettings.logging
        )

        # Create history file if it does not exist
        history_file_path = self.history_file
        if not os.path.exists(history_file_path):
            with open(history_file_path, "a+", encoding="utf-8") as file:
                file.close()

        readline.read_history_file(history_file_path)
        readline.set_history_length(self.history_length)
        atexit.register(readline.write_history_file, history_file_path)

        # Activate command line
        self.activate_command_line = True

        # Log interpreter initialization
        LogManager.instance.log("Interpreter initialized.")

    def exception_message(self, exception: Exception) -> None:
        """ Display exception message """

        trace: list[str] = traceback.format_tb(exception.__traceback__)

        # Prints the full traceback
        print_error("An error occurred...")
        printf()

        line_count = 0
        for line in trace:
            printf(f" ({line_count}) -> {line}")
            line_count += 1

    def prompt(self) -> str:
        """ Creates a command line prompt """

        # Returns basic prompt if no module is loaded
        if Module.module is None:
            return (
                f"\001\x1b[4m\002{ConsoleSettings.prompt_user}\001\x1b[0m\002"
                f" {ConsoleSettings.prompt_symbol} "
            )

        # Creates a module prompt
        module_name: str = Module.module.info["Name"]
        if Module.module_path.startswith("modules"):
            folder: str = Module.module_path.split("/")[1]
        else:
            folder: str = Module.module_path.split("/")[0]

        # Returns the crafted module prompt
        return (
            f"\001\x1b[4m\002{ConsoleSettings.prompt_user}\001\x1b[0m\002 "
            f"{folder}(\001\x1b[1m\x1b[31m\002{module_name}\001\x1b[0m\002) "
            f"{ConsoleSettings.prompt_symbol} "
        )

    def parse_line(self, line: str) -> tuple[str, dict[str, str]]:
        """ Parse a command line into a command and its arguments """
        if not line:
            return "", {}

        command, *args = line.strip().split(maxsplit=1)
        arguments = args[0].split() if args else []

        return command, {
            f"arg{idx+1}": arg for idx, arg in enumerate(arguments)
        }

    def main(self) -> None:
        """ Start the command line interface """
        display_banner()

        # The main command loop
        while self.activate_command_line is True:
            try:
                command, kwargs = self.parse_line(input(self.prompt()))

                # Check for termination commands
                if command in self.terminate_command:
                    self.terminate(command, kwargs)
                    return
                elif hasattr(Command, f"command_{command}"):
                    getattr(Command, f"command_{command}")(self, **kwargs)
                else:
                    self.shell_exec(command, kwargs=kwargs)

            except TerasploitException as e:
                self.exception_message(e)
                LogManager.instance.log(str(e), level="ERROR")

            except Exception as e:
                self.exception_message(e)
                LogManager.instance.log(str(e), level="ERROR")

    def terminate(self, command: str, kwargs: dict[str, Any]) -> None:
        """ Handle the termination of the command line interface """

        # Check for invalid arguments
        if kwargs:
            print_error(f"The {command} command does not accept arguments.")
            return

        # Check for active sessions
        if Session.sessions:
            print_warning(
                f"There are {len(Session.sessions)}"
                " currently active session(s), "
                "terminate all session before exiting."
            )
            print_status(
                'Use the command "kill all" to terminate all sessions.'
                )
            return

        # Log the exit
        LogManager.instance.log("Console terminated")

        # Stop the command line interface
        self.activate_command_line = False

    def shell_exec(self, command: str, **kwargs: dict[str, Any]) -> None:
        """ Execute a command in the system shell """
        if command == "exec":
            print_error(
                f'Unknown command "{command}", use "help" for more details.'
            )
            return

        # Construct the full command
        if kwargs:
            arguments = [str(value) for value in kwargs.values()]
            full_command = " ".join([command] + arguments)
        else:
            full_command = command

        # Execute the command
        try:
            result = subprocess.run(
                shlex.split(full_command),
                stdout=subprocess.PIPE,
                check=False,
                text=True,
            )

            # Check for errors
            if result.returncode != 0:
                raise InvalidError(
                    "An error occurred during shell execution."
                )

            # Check for output
            if result.stdout:
                print_status(f"Executed: {full_command}\n")
                printf(result.stdout)

        except FileNotFoundError:
            print_error(
                f'Unknown command "{command}", use "help" for more details.'
            )

        except ValueError as error:
            print_error(f"Exec error: {error}")
