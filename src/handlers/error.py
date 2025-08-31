# -*- coding: utf-8 -*-

# Python lib
from typing import Any
from functools import wraps

# Console src
from src.utils.printer import print_error


def err_decorator(default_return: Any = None):
    """A decorator to handle errors in functions."""

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # Placing the function inside a try-exception
            # block to catch the error.
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print_error(f"error: {func.__name__} failed: {e}")
                return default_return
        return wrapper
    return decorator
