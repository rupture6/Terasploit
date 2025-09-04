# -*- coding: utf-8 -*-

# Python library
import importlib
import time
import socket
from typing import Any

# Library
from lib.container.module import Module
from lib.utils.exception import InvalidError

# Multiple Imports from Library
from lib.utils.printer import (
    printf,
    print_status,
    print_error,
    print_warning
)
from lib.utils.table import (
    print_module_path_table,
    print_basic_table
)
from lib.utils.decorator import (
    enforce_kwarg_count,
    module_required,
    check_missing_options
)
from lib.utils.path import (
    module_list,
    search_modules,
    modulize_path,
    humanize_path
)

# Framework
from framework.console.options import Opt, OptGet
from framework.console.banner import display_banner
from framework.console.command.metadata import CommandMetadata
from framework.exploit.driver import ExploitDriver
from framework.sessions.thread_handler import Session


class Utils:
    """ Utility function for Command class """

    @staticmethod
    def display_module(parameter: Any) -> None:
        """ Show exploit options """

        # Show all modules if parameter is "all"
        if parameter == "all":
            printf("\n" + "Show: all modules" + "\n")

            # Prints the result in table
            print_module_path_table(module_list())

        # Search for related module if parameter is context-specific
        else:
            printf("\n" + f"Show: {parameter}" + "\n")

            # Prints the result in table
            print_module_path_table(
                search_modules(parameter),
                highlight_term=parameter
            )


class Command:
    """ Base class for all commands """

    # --- Alias Command Category ---

    @enforce_kwarg_count(0)
    def command_options(self):
        """ Alias of command `show options` """
        # NOTE: implement command later
        pass

    # --- Core Command Category ---

    @enforce_kwarg_count(0)
    def command_banner(self) -> None:
        """ Display the console banner """

        # Display the console banner
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

        # Print new line
        printf()

    @enforce_kwarg_count(1)
    def command_get(self, **kwargs: Any) -> None:
        """ Get a value from a context-specific variable """
        keyword: Any = kwargs["arg1"]

        # Display the content of specified key
        printf(f"{keyword} => {OptGet(keyword)}")

    @enforce_kwarg_count(1)
    def command_show(self, **kwargs: Any) -> None:
        """ Display various types of information """
        parameter: Any = kwargs["arg1"]

        # Check if the parameter is a module category
        if parameter in ["auxiliary", "encoder", "exploit", "payload", "all"]:
            Utils.display_module(parameter)
            return

        # Get the function of parameter
        func = getattr(self, f"show_{parameter}", None)

        # Check if parameter function exists
        if func is None:
            raise InvalidError(f'Invalid parameter: {parameter}.')

        # Execute the function of parammeter if it exists
        func()

    # --- Module Command Category ---

    @enforce_kwarg_count(1)
    def command_search(self, **kwargs: Any) -> None:
        """ Search for modules by matching string patterns """
        module_name = kwargs["arg1"]

        # Search module
        modules = search_modules(module_name)

        # Header of the command `search`
        header = "\n" + f"Search: {module_name}" + "\n"

        # Display the header and result of search
        printf(header)
        print_module_path_table(
            modules,
            highlight_term=module_name
        )

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

    @enforce_kwarg_count(1)
    def command_use(self, **kwargs: Any):
        """ Loads and configures a module """
        module_path_arg = kwargs["arg1"]

        # Formats module path
        pythonized_module_path = modulize_path(module_path_arg)

        # Resets options to their default values
        Opt.reset_to_default()

        # Imports the module using python importlib library
        try:
            module = importlib.import_module(pythonized_module_path)
        except ImportError as err:
            print_error(err)
            return

        # Checks if the module imported is a terasploit module
        if not hasattr(module, "TerasploitModule"):
            raise TypeError("The specified module is not a Terasploit module.")

        # The terasploit module
        terasploit_module = getattr(module, "TerasploitModule")()

        if not hasattr(terasploit_module, "info"):
            print_warning("Module information is missing.")

        # Sets current module
        Module.module = terasploit_module
        Module.module_path = humanize_path(pythonized_module_path)

        # Sets default module options
        default_options = terasploit_module.info.get("DefaultOptions", None)
        if default_options:
            Opt.registered_module_options.extend(default_options)

        # Sets default payload
        default_payload = terasploit_module.info.get("DefaultPayload", None)
        if not default_payload:
            return

        try:
            payload_module = importlib.import_module(
                modulize_path("modules/payload/" + default_payload.lstrip("/"))
            )
        except ImportError as err:
            print_error(err)
            return

        if not hasattr(payload_module, "TerasploitModule"):
            raise TypeError("Imported payload is not a Terasploit module.")

        # Initialize the payload
        Module.payload = getattr(payload_module, "TerasploitModule")()

        # Set current payload
        Module.payload_path = humanize_path(
            modulize_path("modules/payload/" + default_payload.lstrip("/"))
        )
        print_status("Configured payload: " + default_payload)

        # Set default payload options
        payload_options = Module.payload.info.get("DefaultOptions", None)
        if payload_options:
            Opt.registered_payload_options.extend(payload_options)

        # Check for exploit target
        if Module.module_path.startswith("modules/exploit"):
            targets = terasploit_module.info.get("Target", None)
            if targets:
                for key, value in targets.items():
                    Opt.exploit_target[key] = value
                    break

        # Check for auxiliary mode
        if Module.module_path.startswith("modules/auxiliary"):
            modes = terasploit_module.info.get("Mode", None)
            if modes:
                for key, value in modes.items():
                    Opt.auxiliary_mode[key] = value
                    break

    @module_required
    @enforce_kwarg_count(0)
    @check_missing_options
    def command_exploit(self):
        """ Executes the currently loaded exploit module """

        # Starts the exploit driver
        ExploitDriver()

    @module_required
    @enforce_kwarg_count(0)
    @check_missing_options
    def command_run(self):
        """ Execute the run method of the currently loaded module """

        # Check if the currently loaded module has a run method
        if hasattr(Module.module, "run"):
            Module.module.run()

        # Raise an invalid error if current module has no run method
        raise InvalidError("Current module doesn't have a run method.")

    @module_required
    @enforce_kwarg_count(0)
    @check_missing_options
    def command_check(self):
        """ Execute the check method of the currently loaded module """

        # Check if the currently loaded module has a check method
        if hasattr(Module.module, "check"):
            Module.module.check()

        # Raise an invalid error if current module has no check method
        raise InvalidError("Current module doesn't have a check method.")

    # --- Jobs Command Category ---

    @enforce_kwarg_count(0)
    def command_list(self):
        """ List jobs that currently exists """

        # Return if no active jobs available
        if not Session.sessions:
            print_status("No currently active jobs.")
            return

        # Session ID and Address
        sn_id = [str(count) for count in range(1, len(Session.sessions) + 1)]
        sn_addr = [str((sess[1], sess[2])) for sess in Session.sessions]

        # Display the sessions in table format
        printf("\n" + "Active Jobs:" + "\n")
        print_basic_table(
            col1_header="Id",
            col2_header="Address",
            col1=sn_id,
            col2=sn_addr
        )

        # Display footer
        printf(
            "\n"
            "Interact with a job by its \"ID\" using the interact command."
            "\n"
        )

    @enforce_kwarg_count(1)
    def command_interact(self, **kwargs: Any):
        """ Interact with a job by its id """
        sn_id = kwargs["arg1"]

        # Return if no active jobs available
        if not Session.sessions:
            print_status("No currently active jobs.")
            return

        # Check if the specified session id exists
        IDs = [str(count) for count in range(1, len(Session.sessions) + 1)]
        if sn_id not in IDs:
            raise TypeError("Session id does not exist.")

        # Display small information
        print_status(
            "Interacting with... "
            f"{Session.sessions[int(sn_id) - 1][1][0]}:"
            f"{Session.sessions[int(sn_id) - 1][1][1]}\n"
        )

        # Starts the session
        exploit_session = Module.payload.info["Session"]
        exploit_session(Session.sessions[int(sn_id) - 1][0])

    @enforce_kwarg_count(1)
    def command_kill(self, **kwargs: Any):
        """ Kill all or specific jobs that is currently active """
        sn_id = kwargs["arg1"]

        # Return if no active jobs available
        if not Session.sessions:
            print_status("No currently active jobs.")
            return

        # Terminates all active sessions
        if sn_id == "all":
            try:
                print_status("Terminating all jobs...")
                Session.alive.set()
                while Session.sessions:
                    time.sleep(0.5)

                Session.reset_events()
                print_status("All jobs have been terminated.")
                return
            except KeyboardInterrupt:
                print_status("Interrupt signal...")
                return

        # Check if the specified session id exists
        IDs = [str(count) for count in range(1, len(Session.sessions) + 1)]
        if sn_id not in IDs:
            raise TypeError("Session id does not exist.")

        # Terminate a specific job
        print_status(f"Terminating job id {sn_id}...")
        sn_count = len(Session.sessions)

        # Shutdown and close the socket of session
        Session.sessions[int(sn_id) - 1][0].shutdown(socket.SHUT_RDWR)
        Session.sessions[int(sn_id) - 1][0].close()

        while len(Session.sessions) == sn_count:
            time.sleep(0.5)

        print_status(f"Job id {sn_id} has been terminated.")
