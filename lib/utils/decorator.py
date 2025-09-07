# -*- coding: utf-8 -*-

# Python library
from functools import wraps
from typing import Any

# Libraryrary
from lib.utils.printer import printf
from lib.utils.exception import InvalidError
from lib.container.module import Module

# Framework
from framework.console.options import Opt


def module_required(func: Any) -> Any:
    """Ensure that a module is selected before executing the function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        # Check if a module has been loaded into Module.module
        if not Module.module:

            # Raise error if no module is set
            raise InvalidError("Action requires a module to run.")

        # If a module is set, execute the original function
        return func(*args, **kwargs)
    return wrapper


def enforce_kwarg_count(expected_count: int) -> Any:
    """ Ensure a function is called with a specific number of kwargs """
    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # Verify that the number of keyword arguments matches expectation
            if len(kwargs) != expected_count:

                # Get a more readable function name for the error message
                function_name = func.__name__.replace("_", " ").capitalize()

                # Raise TypeError with details about mismatch
                raise TypeError(
                    f"{function_name} expect: {expected_count} " +
                    f"argument(s), but got {len(kwargs)}."
                )

            # If the number of kwargs is correct, run the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_missing_options(func: Any) -> Any:
    """ Ensure all required options are set before running the function """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        # Counter for missing required options
        missing = 0

        # Combine both module and payload options into one list
        options = Opt.registered_module_options.copy()
        options.extend(Opt.registered_payload_options.copy())

        # Loop through all options and check required ones
        for opt_name in options:

            # Skip if the option is not marked as required
            if str(Opt.required[opt_name]).lower() != "yes":
                continue

            # If required option is missing or empty, print error
            if not Opt.options[opt_name]:
                printf(f"error => {opt_name}: null")
                missing += 1

        # If any required options are missing, stop execution
        if missing > 0:
            return None

        # Otherwise, execute the original function
        return func(*args, **kwargs)
    return wrapper
