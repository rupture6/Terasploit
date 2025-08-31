# -*- coding: utf-8 -*-

# Python lib
import os
import readline
import atexit
import traceback

# Console src
from src.utils.printer import print_error, printf
from src.container.module import Module
from src.container.console import Setting, Logging
from src.utils.exception import TerasploitException

# Framework
from framework.console.banner import display_banner
from framework.console.logs import Log


class Interpreter:
    """The main interpreter class."""

    # Activates and deactivates the command line interface
    activate_command_line: bool = False

    # History file and length
    history_length: int = 100
    history_file: str = os.path.join(
        os.path.expanduser("~"),
        ".tera_history"
    )

    def __init__(self) -> None:
        """Initialize the interpreter."""

        # Initialize logging
        Logging.instance = Log(
            logfile="terasploit.log",
            level=Setting.log_level,
            console=Setting.logging
        )

        Logging.instance.log("Interpreter initialized.")

        # Create history file if it does not exist
        history_file_path = self.history_file
        if not os.path.exists(history_file_path):
            with open(history_file_path, "a+", encoding="utf-8") as file:
                file.close()

        readline.read_history_file(history_file_path)
        readline.set_history_length(self.history_length)
        atexit.register(readline.write_history_file, history_file_path)

        self.activate_command_line = True

    def exception_message(self, exception: Exception) -> None:
        """Display exception message."""

        trace: list[str] = traceback.format_tb(exception.__traceback__)

        # Prints the full traceback
        print_error("An error occurred...")
        printf()

        line_count = 0
        for line in trace:
            printf(f" ({line_count}) -> {line}")
            line_count += 1

    def prompt(self) -> str:
        """Creates a command line prompt."""

        # Returns basic prompt if no module is loaded
        if Module.module is None:
            return (
                f"\001\x1b[4m\002{Setting.prompt_user}\001\x1b[0m\002 "
                f"{Setting.prompt_char} "
            )

        # Creates a module prompt
        module_name: str = Module.module.info["Name"]
        if Module.module_path.startswith("modules"):
            folder: str = Module.module_path.split("/")[1]
        else:
            folder: str = Module.module_path.split("/")[0]

        # Returns the crafted module prompt
        return (
            f"\001\x1b[4m\002{Setting.prompt_user}\001\x1b[0m\002 "
            f"{folder}(\001\x1b[1m\x1b[31m\002{module_name}\001\x1b[0m\002) "
            f"{Setting.prompt_char} "
        )

    def parse_line(self, line: str) -> tuple[str, dict[str, str]]:
        """Parse a command line into a command and its arguments."""

        if not line:
            return "", {}

        command, *args = line.strip().split(maxsplit=1)
        arguments = args[0].split() if args else []

        return command, {
            f"arg{idx+1}": arg for idx, arg in enumerate(arguments)
        }

    def main(self) -> None:
        """Start the command line interface."""

        # Displays the banner first
        display_banner()

        # The main command loop
        while self.activate_command_line is True:
            try:
                command, kwargs = self.parse_line(input(self.prompt()))
                printf(f"Command: {command}, Arguments: {kwargs}")

            except TerasploitException as e:
                self.exception_message(e)
                Logging.instance.log(str(e), level="ERROR")

            except Exception as e:
                self.exception_message(e)
                Logging.instance.log(str(e), level="ERROR")
