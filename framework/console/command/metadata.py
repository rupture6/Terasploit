# -*- coding: utf-8 -*-

# Python library
from typing import ClassVar


class CommandMetadata:
    """ All commands and usage information in one structure """

    command_category: list[str] = ["Core", "Module", "Alias", "Jobs"]

    commands: ClassVar[dict[str, dict[str, str]]] = {
        "Alias": {
            "quit": "Alias of exit command",
            "terminate": "Alias of exit command",
            "done": "Alias of exit command",
            "close": "Alias of exit command",
            "options": 'Alias of "show options" command',
        },
        "Core": {
            "help": "Display command descriptions",
            "banner": "Display Terasploit banner",
            "show": "Show content from a context-specific parameter",
            "unset": "Remove a value from a context-specific variable",
            "set": "Set a value to a context-specific variable",
            "get": "Get a value from a context-specific variable",
            "exit": "Exit the Terasploit console",
        },
        "Module": {
            "run": "Execute non-exploit module",
            "exploit": "Execute exploit module",
            "check": "Execute check function of the module",
            "use": "Interact with a module by its path",
            "search": "Search a module path via matching strings",
            "back": "Exit current module context",
            "info": "Display module information",
        },
        "Jobs": {
            "list": "List running jobs",
            "kill": "Kill a job by its ID",
            "interact": "Interact with a job by its ID",
        },
    }

    usages: ClassVar[dict[str, dict[str, list[str]]]] = {
        "info": {
            "Usage: info [path]": [
                "Displays full information of the module."
            ],
            "Example:": [
                "info exploit/multi/handler"
            ],
        },
        "use": {
            "Usage: use [module_path]": [
                "Allows interaction with a module to perform its task."
            ],
            "Example:": [
                "use exploit/multi/handler"
            ],
        },
        "set": {
            "Usage: set [variable] [value]": [
                "Sets a value to a context-specific variable with validation."
            ],
            "Example:": [
                "set rhost 192.168.0.1"
            ],
        },
        "unset": {
            "Usage: unset [parameter]": [
                "Removes a value from a context-specific variable."
            ],
            "Example:": [
                "unset rhost"
            ],
        },
        "show": {
            "Usage: show [parameter]": [
                "Displays content from a context-specific parameter."
            ],
            "Parameter:": [
                "all, options, auxiliary, encoder,"
                " "
                "exploit, payload, targets, modes"
            ],
            "Example:": [
                "show all"
            ],
        },
        "search": {
            "Usage: search [pattern]": [
                "Searches for a module path via matching strings."
            ],
            "Example:": [
                "search exploit/"
            ],
        },
    }
