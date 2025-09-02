# -*- coding: utf-8 -*-

# Python lib
from typing import Any
from functools import wraps

# Lib
from lib.utils.printer import print_error


def error_handler(
    default_return: Any = None,
    expected_error: Any = Exception
):
    """A decorator to handle errors in functions."""

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except expected_error as e:
                print_error(f"error: {func.__name__} info: {e}")
                if callable(default_return):
                    return default_return()
                else:
                    return default_return
        return wrapper
    return decorator
