# -*- coding: utf-8 -*-

# Python library
from typing import Any
from functools import wraps

# Library
from lib.utils.printer import print_error


def check_default_return(default_return: Any) -> Any:
    """ Check if default_return is a callable or a static value """
    if callable(default_return):
        return default_return()

    # Static value
    return default_return


def error_handler(
    default_return: Any = None,
    expected_error: Any = Exception
):
    """ A decorator to handle errors in functions """
    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except expected_error as e:
                print_error(f"error: {func.__name__} info: {e}")
                return check_default_return(default_return)
        return wrapper
    return decorator
