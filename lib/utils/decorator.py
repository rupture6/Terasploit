# -*- coding: utf-8 -*-

# Python lib
from functools import wraps
from typing import Any

# Lib
from lib.utils.printer import printf
from lib.utils.exception import InvalidError
from lib.container.module import Module

# Framework
from framework.console.options import Opt


def module_required(func: Any) -> Any:
    """Ensure that a module is selected before executing the function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not Module.module:
            raise InvalidError(
                "Function requires a module to run.",
                "Module is not selected."
            )
        return func(*args, **kwargs)
    return wrapper


def enforce_kwarg_count(expected_count: int) -> Any:
    """Ensure a function is called with a specific number of kwargs."""
    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if len(kwargs) != expected_count:
                function_name = func.__name__.replace("_", " ").capitalize()
                raise TypeError(
                    f"{function_name} expects {expected_count} "
                    f"argument(s), but got {len(kwargs)}."
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_missing_options(func: Any) -> Any:
    """Ensure all required options are set before running the function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        missing = 0

        options = Opt.registered_module_options.copy()
        options.extend(Opt.registered_payload_options.copy())

        for opt_name in options:
            if str(Opt.required[opt_name]).lower() != "yes":
                continue
            if not Opt.options[opt_name]:
                printf(f"ERROR => {opt_name}: NULL")
                missing += 1

        if missing > 0:
            return None
        return func(*args, **kwargs)
    return wrapper
