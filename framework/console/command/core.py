# -*- coding: utf-8 -*-

# Python library
from typing import Any

# Library
from lib.container.module import Module
from lib.utils.path import module_list, search_modules
from lib.utils.printer import printf
from lib.utils.table import print_module_path_table
from lib.utils.decorator import (
    enforce_kwarg_count,
    module_required
)

# Framework
from framework.console.options import Opt
from framework.console.banner import display_banner


class Command:
    """ Base class for all commands """

    def display_module(self, attr: Any) -> None:
        """ Show exploit options """
        if attr == "all":
            printf("\nShow: all modules\n")
            modules = module_list()
            print_module_path_table(modules)
        else:
            printf(f"\nShow: {attr}\n")
            modules = search_modules(attr)
            print_module_path_table(modules, highlight_term=attr)

    @module_required
    @enforce_kwarg_count(0)
    def command_back(self):
        """ Unloads the currently loaded module """

        # Resets options to their default values
        Opt.reset_to_default()

        # Clears the modules variables
        Module.module = None
        Module.module_path = None

        Module.payload = None
        Module.payload_path = None

        Module.encoder = None
        Module.encoder_path = None

    @enforce_kwarg_count(0)
    def command_banner(self) -> None:
        """ Display the command banner """
        display_banner()

    @enforce_kwarg_count(0)
    def command_help(self) -> None:
        """ Display the command help """
        # TODO: Implement help command output
        pass

    @enforce_kwarg_count(1)
    def command_get(self, **kwargs: Any) -> None:
        """ Get a value from a context-specific variable """
        keyword: Any = kwargs["arg1"]
        printf(f"{keyword} => {Opt.options.get(keyword)!r}")

    @enforce_kwarg_count(1)
    def command_show(self, **kwargs: Any) -> None:
        """ Display various types of information """
        attribute: Any = kwargs["arg1"]
        if attribute in ["auxiliary", "encoder", "exploit", "payload", "all"]:
            self.display_module(attribute)
            return

        handler = getattr(self, f"show_{attribute}", None)
        if handler is None:
            raise TypeError(
                f'"show" command received an invalid parameter: {attribute}'
            )
        handler()

    @enforce_kwarg_count(1)
    def command_search(self, **kwargs: Any) -> None:
        """ Search for modules by matching string patterns """
        module_name = kwargs["arg1"]
        modules = search_modules(module_name)

        printf(f"\nSearch: {module_name}\n")
        print_module_path_table(modules, highlight_term=module_name)
