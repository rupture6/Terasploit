# -*- coding: utf-8 -*-

# Python lib
import sys
from typing import Any, TextIO

# Console lib
from src.container.console import Setting


class ConsolePrinter:
    """Handles printing messages with optional colors and verbosity."""

    def __init__(
        self,
        *args: Any,
        sep: str = " ",
        end: str = "\n",
        file: TextIO = sys.stdout,
        flush: bool = False,
        verbose: bool = Setting.verbose,
        prefix: str = "",
    ) -> None:
        if not verbose:
            return
        message = f"{prefix} {sep.join(str(arg) for arg in args)}".strip()
        file.write(message + end)
        if flush:
            file.flush()


# Core print functions
def printf(*args: Any, **kwargs: Any) -> None:
    """Generic print function."""
    ConsolePrinter(*args, **kwargs)


def print_error(*args: Any, **kwargs: Any) -> None:
    """Prints messages with a red '[-]' prefix."""
    ConsolePrinter(*args, prefix="\033[1;31m[-]\033[0m", **kwargs)


def print_warning(*args: Any, **kwargs: Any) -> None:
    """Prints messages with a yellow '[!]' prefix."""
    ConsolePrinter(*args, prefix="\033[1;33m[!]\033[0m", **kwargs)


def print_result(*args: Any, **kwargs: Any) -> None:
    """Prints messages with a green '[+]' prefix."""
    ConsolePrinter(*args, prefix="\033[1;32m[+]\033[0m", **kwargs)


def print_status(*args: Any, **kwargs: Any) -> None:
    """Prints messages with a blue '[*]' prefix."""
    ConsolePrinter(*args, prefix="\033[1;34m[*]\033[0m", **kwargs)
