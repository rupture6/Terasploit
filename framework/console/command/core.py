# -*- coding: utf-8 -*-

# Python library
from typing import Any

# Library
from lib.container.module import Module
from lib.utils.path import module_list, search_modules
from lib.utils.printer import printf
from lib.utils.table import print_module_path_table, print_basic_table
from lib.utils.decorator import enforce_kwarg_count, module_required
from lib.utils.exception import InvalidError

# Framework
from framework.console.options import Opt, OptGet
from framework.console.banner import display_banner
from framework.console.command.metadata import CommandMetadata


class Utils:
    """ Utility function for Command class """

    @staticmethod
    def display_module(param: Any) -> None:
        """Show exploit options."""

        # Show all modules if parameter is "all"
        if param == "all":
            printf("\n" + "Show: all modules" + "\n")

            # Prints the result in table
            print_module_path_table(module_list())

        # Search for related module if parameter is context-specific
        else:
            printf("\n" + f"Show: {param}" + "\n")

            # Prints the result in table
            print_module_path_table(
                search_modules(param),
                highlight_term=param
            )


class Command:
    """ Base class for all commands """

    @module_required
    @enforce_kwarg_count(0)
    def command_back(self) -> None:
        """ Unload the currently loaded module """

        # Reset options to their default values
        Opt.reset_to_default()

        # Clear module variables
        _list: list[str] = [
            "module",
            "payload",
            "encoder"
        ]

        # Set None value in module class variable
        for i in _list:
            setattr(Module, i, None)
            setattr(Module, f"{i}_path", None)

    @enforce_kwarg_count(0)
    def command_banner(self) -> None:
        """ Display the console banner """
        display_banner()

    @enforce_kwarg_count(0)
    def command_help(self) -> None:
        """ Display the command help """
        category = CommandMetadata.command_category

        # Displays the command description on each command category
        for c in category:
            header = "\n" + c + " Command"

            # Display the header
            printf(header)
            print("=" * int(len(header) - 1), "\n")

            # Contents of command category
            contents = CommandMetadata.commands[c]

            # Display the content in table
            print_basic_table(
                col1_header="Command",
                col1=list(contents.keys()),
                col2=list(contents.values()),
                col1_width=15
            )

        # New line
        printf()

    @enforce_kwarg_count(1)
    def command_get(self, **kwargs: Any) -> None:
        """ Get a value from a context-specific variable """
        keyword: Any = kwargs["arg1"]
        printf(f"{keyword} => {OptGet(keyword)}")

    @enforce_kwarg_count(1)
    def command_show(self, **kwargs: Any) -> None:
        """ Display various types of information """
        attribute: Any = kwargs["arg1"]
        if attribute in ["auxiliary", "encoder", "exploit", "payload", "all"]:
            Utils.display_module(attribute)
            return

        handler = getattr(self, f"show_{attribute}", None)
        if handler is None:
            raise InvalidError(
                f'"show" command received an invalid parameter: {attribute}'
            )
        handler()

    @enforce_kwarg_count(1)
    def command_search(self, **kwargs: Any) -> None:
        """ Search for modules by matching string patterns """
        module_name = kwargs["arg1"]
        modules = search_modules(module_name)

        printf("\n" + f"Search: {module_name}" + "\n")
        print_module_path_table(modules, highlight_term=module_name)
