# -*- coding: utf-8 -*-

# Python library
from typing import Any


class Config:
    """ Centralized console configuration """

    # Names of class variable in list
    names = [
        "logging",
        "verbose",
        "prompt_symbol",
        "prompt_user"
    ]
    require = [
        "no",
        "no",
        "no",
        "no"
    ]
    description = [
        "Enable or disable console logging",
        "Set the verbosity level of console output",
        "Symbol displayed in the console prompt",
        "Username displayed in the console prompt"
    ]

    # Logging configuration
    logging: bool = False

    # Verbosity configuration
    verbose: bool = True

    # Prompt configuration
    prompt_symbol: str = ">"
    prompt_user: str = "tsf"


class Logger:
    """ Global logger instance manager """

    instance: Any = None
