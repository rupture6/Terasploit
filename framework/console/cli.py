# -*- coding: utf-8 -*-

# Python lib
import os
import readline
import atexit
import traceback

# Console src
from src.utils.printer import print_error, printf


class Interpreter:
    """The main interpreter class."""

    # Activates and deactivates the command line interface
    activate_command_line: bool = False

    # History file and length
    history_file: str = os.path.join(os.path.expanduser("~"), ".tsf_history")
    history_length: int = 100

    def __init__(self) -> None:
        """Initialize the interpreter.

        This sets up the interpreter, including initializing the history file
        and setting up the readline library.
        """

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

        # The traceback of the exception
        header = traceback.format_exception_only(
            type(exception),
            exception
        )[0].strip()
        trace = traceback.format_tb(exception.__traceback__)

        # Prints the full traceback
        print_error("An exception occurred... verbose is true.")
        print_error(header + "\n")

        for line in trace:
            printf(f" => {line}")
        printf()

        # Print exception message then return
        print_error(str(exception))
