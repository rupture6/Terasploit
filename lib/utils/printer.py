# -*- coding: utf-8 -*-

# Python library
import sys
from typing import Any, TextIO

# Console src


class ConsolePrinter:
    """ Handles printing messages with optional colors and verbosity """

    def __init__(
        self,
        *args: Any,
        sep: str = " ",
        end: str = "\n",
        file: TextIO = sys.stdout,
        flush: bool = False,
        verbose: bool = True,
        prefix: str = "",
    ) -> None:
        """ Initialize the printer with given parameters """

        # Return if verbose is false
        if not verbose:
            return

        self.prefix: str = prefix
        self.args: Any = args
        self.sep: str = sep
        self.end: str = end
        self.file: Any = file
        self.flush: bool = flush

        self._print()

    def _print(self) -> None:
        """ Main print function """
        if not self.file:
            return

        sep: str = " " if not self.sep else self.sep
        end: str = "\n" if not self.end else self.end

        # Writes the content of the print
        if self.prefix:
            self.file.write(self.prefix + " ")

        for i, arg in enumerate(self.args):
            if i:
                self.file.write(str(sep))
            self.file.write(str(arg))
        self.file.write(str(end))

        if self.flush is True:
            self.file.flush()


# Core print functions
def printf(*args: Any, **kwargs: Any) -> None:
    """ Generic print function """
    ConsolePrinter(*args, **kwargs)


def print_error(*args: Any, **kwargs: Any) -> None:
    """ Prints messages with a red '[-]' prefix """
    ConsolePrinter(*args, prefix="\033[1;31m[-]\033[0m", **kwargs)


def print_warning(*args: Any, **kwargs: Any) -> None:
    """ Prints messages with a yellow '[!]' prefix """
    ConsolePrinter(*args, prefix="\033[1;33m[!]\033[0m", **kwargs)


def print_result(*args: Any, **kwargs: Any) -> None:
    """ Prints messages with a green '[+]' prefix """
    ConsolePrinter(*args, prefix="\033[1;32m[+]\033[0m", **kwargs)


def print_status(*args: Any, **kwargs: Any) -> None:
    """ Prints messages with a blue '[*]' prefix """
    ConsolePrinter(*args, prefix="\033[1;34m[*]\033[0m", **kwargs)
