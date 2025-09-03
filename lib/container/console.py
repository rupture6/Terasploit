# -*- coding: utf-8 -*-

# Python library
from typing import Any


class ConsoleSettings:
    """ Default configuration for the console """

    # Logging configuration
    logging: bool = True
    log_level: str = "INFO"

    # Verbosity configuration
    verbose: bool = True

    # Prompt configuration
    prompt_symbol: str = ">"
    prompt_user: str = "tsf"


class LogManager:
    """ Holds the global logging instance """
    instance: Any = None
