# -*- coding: utf-8 -*-

# Python library
from typing import Any, Literal


class Config:
    """ Centralized console configuration """

    # Logging configuration
    logging: bool = False
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    ] = "INFO"

    # Verbosity configuration
    verbose: bool = True

    # Prompt configuration
    prompt_symbol: str = ">"
    prompt_user: str = "tsf"


class Logger:
    """ Global logger instance manager """

    instance: Any = None
