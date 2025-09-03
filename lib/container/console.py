# -*- coding: utf-8 -*-

# Python library
from typing import Any


class Config:
    """ Centralized console configuration """

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
