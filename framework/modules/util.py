# -*- coding: utf-8 -*-

# Python library
from typing import Any

# Framework
from framework.console.options import Opt


def register_option(options: list[Any]) -> None:
    """ Register module options in the global options database """

    for option in options:
        key = option.name.upper()

        # Track option key for module scope
        Opt.registered_module_options.append(key)

        # Store option metadata
        Opt.default[key] = option.default
        Opt.options[key] = option.default
        Opt.description[key] = option.description
        Opt.required[key] = option.required
        Opt.validator[key] = option.validator
