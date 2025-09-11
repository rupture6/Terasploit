# -*- coding: utf-8 -*-

# Python library
import importlib
import time
import socket
from typing import Any

# Library
from lib.container.console import Config
from lib.container.module import Module

# Library multiple imports
from lib.utils.printer import (
    printf,
    print_status,
    print_error,
    print_warning
)
from lib.utils.table import (
    print_module_path_table,
    print_basic_table,
    print_options_table
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
    humanize_path,
    parse_python_path
)
from lib.utils.exception import (
    InvalidError,
    ValidationError
)

# Framework
from framework.console.banner import display_banner
from framework.console.command.metadata import CommandMetadata
from framework.exploit.driver import ExploitDriver
from framework.sessions.core.thread_handler import Session

# Framework multiple imports
from framework.console.options import (
    Opt,
    OptGet
)


class Utils:
    """ Utility functions used by the Command class """

    def display_module(self, parameter: Any) -> None:
        """ Display exploit, payload, encoder, or auxiliary modules """

        # Show all modules if parameter is "all"
        if parameter == "all":
            printf("\n" + "Show: all modules" + "\n")

            # Prints all modules in a table
            print_module_path_table(module_list())

        # Otherwise, search for modules by parameter keyword
        else:
            printf("\n" + f"Show: {parameter}" + "\n")

            # Prints matching modules in a table, highlighting the search term
            print_module_path_table(
                search_modules(parameter),
                highlight_term=parameter
            )

    def set_module(self, module_path: str) -> None:
        """ Load and set a payload or encoder as the current module """
        path = modulize_path(module_path)

        # Set payload module
        if "payload" in parse_python_path(path):

            # Reset payload options to default
            for i in Opt.registered_payload_options:
                if i not in Opt.default_options:
                    del Opt.options[i]
                else:
                    Opt.options[i] = Opt.default_options[i]

            # Clear any previously registered payload options
            Opt.registered_payload_options.clear()

            # Try importing payload module
            try:
                payload = importlib.import_module(path)
            except ImportError as err:
                print_error(err)
                return

            # Ensure imported module is a valid Terasploit module
            if not hasattr(payload, "TerasploitModule"):
                raise TypeError("Specified module is not a Terasploit module.")

            # Initialize payload object
            terasploit_payload = getattr(payload, "TerasploitModule")()

            # Warn if payload lacks module information
            if not hasattr(terasploit_payload, "info"):
                print_warning("Module information is missing.")

            # Set current payload and its path
            Module.payload = terasploit_payload
            Module.payload_path = humanize_path(path)

            # Register default payload options if available
            opts = terasploit_payload.info.get("DefaultOptions", None)
            if opts:
                Opt.registered_payload_options.extend(opts)

            printf(f"payload => {Module.payload_path.replace('modules/', '')}")
            return

        # Set encoder module
        if "encoder" in parse_python_path(path):

            # Try importing encoder module
            try:
                encoder = importlib.import_module(path)
            except ImportError as err:
                print_error(err)
                return

            # Ensure imported module is a valid Terasploit module
            if not hasattr(encoder, "TerasploitModule"):
                raise TypeError("Specified module is not a terasploit module.")

            # Initialize encoder object
            terasploit_encoder = getattr(encoder, "TerasploitModule")()

            # Set current encoder and its path
            Module.encoder = terasploit_encoder
            Module.encoder_path = humanize_path(path)
            printf(f"encoder => {Module.encoder_path.replace('modules/', '')}")
            return

        # If not payload or encoder, raise error
        raise TypeError("Payload & Encoder can only be set.")

    def print_options(
        self,
        options: list[Any],
        header: str,
        path: str
    ) -> None:
        """ Print a formatted options table """

        # Extract values for each option (convert to str for display)
        values: list[str] = [
            str(Opt.options.get(key)) for key in options
        ]

        # Extract required status (True/False) for each option
        required_status: list[str] = [
            str(Opt.required.get(key)) for key in options
        ]

        # Extract descriptions for each option
        descriptions: list[Any] = [
            Opt.description.get(key) for key in options
        ]

        # Print section header
        printf(f"\n{header} ({path}):\n")

        # Print options in a formatted table
        print_options_table(
            options,
            values,
            required_status,
            descriptions,
        )

    def module_options(self) -> None:
        """ Print all available module options in table format """

        # Module options
        if Opt.registered_module_options:
            self.print_options(
                Opt.registered_module_options,
                "Module options",
                Module.module_path,
            )

        # Payload options
        if Opt.registered_payload_options:
            self.print_options(
                Opt.registered_payload_options,
                "Payload options",
                Module.payload_path,
            )

        # Exploit targets
        if Module.module.info.get("Target"):
            target_ids = list(Opt.exploit_target.keys())
            target_names = [
                Opt.exploit_target[target_id] for target_id in target_ids
            ]

            printf("\nExploit target:\n")
            print_basic_table(
                target_ids,
                target_names,
                col1_header="Id",
                col2_header="Name",
            )

        # Auxiliary modes
        if Module.module.info.get("Mode"):
            mode_ids = list(Opt.auxiliary_mode.keys())
            mode_names = [
                Opt.auxiliary_mode[mode_id] for mode_id in mode_ids
            ]

            printf("\nAuxiliary mode:\n")
            print_basic_table(
                mode_ids,
                mode_names,
                col1_header="Id",
                col2_header="Name",
            )

        # Info hint
        printf(
            '\n'
            'Use the command "info" to display full module information.'
            '\n'
        )

    def config_options(self) -> None:
        """Print the global options table."""

        # Print section header
        printf("\nGlobal options:\n")

        # Gather values set in Config
        values = [getattr(Config, name) for name in Config.names]

        # Print global options in a formatted table
        print_options_table(
            Config.names,
            values,
            Config.require,
            Config.description,
        )

        # Print trailing newline / suffix
        printf()


class Command(Utils):
    """ Base class for all framework console commands """

    # --- Alias Command Category ---

    @enforce_kwarg_count(0)
    def command_options(self):
        """ Alias of command `show options` """
        self.show_options()

    # --- Core Command Category ---

    @enforce_kwarg_count(0)
    def command_banner(self) -> None:
        """ Display the console banner """

        # Show terasploit banner
        display_banner()

    @enforce_kwarg_count(0)
    def command_help(self) -> None:
        """ Display the help menu for all command categories """
        category = CommandMetadata.command_category

        # Loop through each command category
        for c in category:
            header = "\n" + c + " Command"

            # Display section header
            printf(header)
            print("=" * int(len(header) - 1), "\n")

            # Retrieve commands under category
            contents = CommandMetadata.commands[c]

            # Print commands and descriptions in a table
            print_basic_table(
                col1_header="Command",
                col1=list(contents.keys()),
                col2=list(contents.values()),
                col1_width=15
            )

        # Print new line for readability
        printf()

    @enforce_kwarg_count(1)
    def command_get(self, **kwargs: Any) -> None:
        """ Retrieve a value from a specific option """
        keyword: Any = kwargs["arg1"]

        # Display the value of the given key
        printf(f"{keyword} => {OptGet(keyword)}")

    @enforce_kwarg_count(1)
    def command_show(self, **kwargs: Any) -> None:
        """ Display modules or framework-related information """
        parameter: Any = kwargs["arg1"]

        # Check if parameter matches a module category
        if parameter in ["auxiliary", "encoder", "exploit", "payload", "all"]:
            self.display_module(parameter)
            return

        # Try to find function matching parameter
        func = getattr(self, f"show_{parameter}", None)

        # Raise error if parameter is invalid
        if func is None:
            raise InvalidError(f'Invalid parameter: {parameter}.')

        # Execute valid "show" function
        func()

    @enforce_kwarg_count(2)
    def command_set(self, **kwargs: Any) -> None:
        """ Set a value to a context-specific variable """
        keyword = kwargs["arg1"].upper()
        value = kwargs["arg2"]

        # Format value
        formatted_value = Opt.format_value(value)

        # Set and return if keyword exists in Config
        if keyword.lower() in Config.names:
            setattr(Config, keyword.lower(), formatted_value)
            printf(f"{keyword} => {formatted_value}")
            return

        # Handle module-related options
        if keyword in ("PAYLOAD", "ENCODER"):
            self.set_module(value)
            return

        # Handle exploit target options
        if keyword == "TARGET":
            if not Module.module:
                raise InvalidError("No current exploit module in use...")

            target = Module.module.info["Target"].get(str(value))
            if target is not None:
                Opt.clear_target()
                Opt.exploit_target[str(value)] = target
                printf(f"exploit_target => {target}")
                return

            raise InvalidError(f"Unknown exploit target: {value}")

        # Handle auxiliary mode options
        if keyword == "MODE":
            if not Module.module:
                raise InvalidError("No current auxiliary module in use...")

            mode = Module.module.info["Mode"].get(str(value))
            if mode is not None:
                Opt.clear_mode()
                Opt.auxiliary_mode[str(value)] = mode
                printf(f"auxiliary_mode => {mode}")
                return

            raise InvalidError(f"Unknown auxiliary mode: {value}")

        # Validate and set option value if not a global option
        try:
            if Opt.validator[keyword]:
                is_valid: Any = Opt.validator[keyword](formatted_value)
                if is_valid:
                    Opt.options[keyword] = formatted_value
                    printf(f"{keyword} => {formatted_value!r}")
                    return
                else:
                    raise ValidationError(
                        f"Invalid, {keyword} => {formatted_value!r}"
                    )

            # Set if there is no validator
            Opt.options[keyword] = formatted_value
            printf(f"{keyword} => {formatted_value!r}")

        except KeyError:
            Opt.options[keyword] = formatted_value
            printf(f"{keyword} => {formatted_value!r}")

    @enforce_kwarg_count(1)
    def command_unset(self, **kwargs: Any):
        """ Unset a value from a context-specific variable """
        keyword = kwargs["arg1"]
        key = keyword.upper()

        if Opt.default.get(key, None) is not None:
            print_warning(
                "Default value exists; ignoring unset and",
                "reusing the default value instead..."
            )
            Opt.options[key] = Opt.default[key]
            printf(f"{key} => {Opt.options[key]!r}")
        else:
            Opt.options[key] = None
            printf(f"{key} => {Opt.options[key]!r}")

    @module_required
    def show_targets(self) -> None:
        """ Show exploit targets """

        # Ensure current module is an exploit module
        if not Module.module_path.startswith("modules/exploit"):
            raise InvalidError("Current module is not an exploit module.")

        # Print section header
        printf("\nTarget options\n")

        # Collect target IDs and names from module info
        target_ids = list(Module.module.info["Target"].keys())
        target_names = [
            Module.module.info["Target"][target_id] for target_id in target_ids
        ]

        # Print formatted table of targets
        print_basic_table(
            target_ids,
            target_names,
            col1_header="Id",
            col2_header="Name",
        )

    # Print trailing newline / suffix
    printf()

    @module_required
    def show_modes(self) -> None:
        """ Show auxiliary modes """

        # Ensure current module is an auxiliary module
        if not Module.module_path.startswith("modules/auxiliary"):
            raise InvalidError("Current module is not an auxiliary module.")

        # Print section header
        printf("\nModes options\n")

        # Collect mode IDs and names from module info
        mode_ids = list(Module.module.info["Mode"].keys())
        mode_names = [
            Module.module.info["Mode"][mode_id] for mode_id in mode_ids
        ]

        # Print formatted table of modes
        print_basic_table(
            mode_ids,
            mode_names,
            col1_header="Id",
            col2_header="Name",
        )

        # Print trailing newline / suffix
        printf()

    def show_options(self):
        """ Display options for the current context """

        # Check for current context of module
        if Module.module is not None:
            self.module_options()
            return

        # Show config options instead if there is no module
        self.config_options()

    # --- Module Command Category ---

    @enforce_kwarg_count(1)
    def command_search(self, **kwargs: Any) -> None:
        """ Search for modules by keyword pattern """
        module_name = kwargs["arg1"]

        # Perform module search
        modules = search_modules(module_name)

        # Print header and results
        header = "\n" + f"Search: {module_name}" + "\n"
        printf(header)
        print_module_path_table(
            modules,
            highlight_term=module_name
        )

    @module_required
    @enforce_kwarg_count(0)
    def command_back(self) -> None:
        """ Unload the currently active module """

        # Reset all options to default
        Opt.reset_to_default()

        # List of module-related variables to clear
        _list: list[str] = [
            "module",
            "payload",
            "encoder"
        ]

        # Set all module variables to None
        for i in _list:
            setattr(Module, i, None)
            setattr(Module, f"{i}_path", None)

    @enforce_kwarg_count(1)
    def command_use(self, **kwargs: Any):
        """ Load and configure a module """
        module_path_arg = kwargs["arg1"]

        # Convert to Python-importable path
        pythonized_module_path = modulize_path(module_path_arg)

        # Reset options before loading new module
        Opt.reset_to_default()

        # Import requested module
        try:
            module = importlib.import_module(pythonized_module_path)
        except ImportError as err:
            print_error(err)
            return

        # Ensure it's a Terasploit module
        if not hasattr(module, "TerasploitModule"):
            raise TypeError("Specified module is not a terasploit module.")

        # Initialize module
        terasploit_module = getattr(module, "TerasploitModule")()

        # Warn if module lacks info section
        if not hasattr(terasploit_module, "info"):
            print_warning("Module information is missing.")

        # Set current module and its path
        Module.module = terasploit_module
        Module.module_path = humanize_path(pythonized_module_path)

        # Register default module options if provided
        default_options = terasploit_module.info.get("DefaultOptions", None)
        if default_options:
            Opt.registered_module_options.extend(default_options)

        # Load default payload if specified
        default_payload = terasploit_module.info.get("DefaultPayload", None)
        if not default_payload:
            return

        # Import default payload
        try:
            payload_module = importlib.import_module(
                modulize_path("modules/payload/" + default_payload.lstrip("/"))
            )
        except ImportError as err:
            print_error(err)
            return

        # Ensure payload is valid
        if not hasattr(payload_module, "TerasploitModule"):
            raise TypeError("Imported payload is not a Terasploit module.")

        # Initialize payload
        Module.payload = getattr(payload_module, "TerasploitModule")()

        # Save payload path
        Module.payload_path = humanize_path(
            modulize_path("modules/payload/" + default_payload.lstrip("/"))
        )
        print_status("Configured payload: " + default_payload)

        # Register default payload options if available
        payload_options = Module.payload.info.get("DefaultOptions", None)
        if payload_options:
            Opt.registered_payload_options.extend(payload_options)

        # Handle exploit target configuration
        if Module.module_path.startswith("modules/exploit"):
            targets = terasploit_module.info.get("Target", None)
            if targets:
                for key, value in targets.items():
                    Opt.exploit_target[key] = value
                    break

        # Handle auxiliary mode configuration
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
        """ Execute the currently loaded exploit module """

        # Start the exploit driver
        ExploitDriver()

    @module_required
    @enforce_kwarg_count(0)
    @check_missing_options
    def command_run(self):
        """ Execute the `run` method of the currently loaded module """

        # Run the module if `run` method exists
        if hasattr(Module.module, "run"):
            Module.module.run()
            return

        # Otherwise raise error
        raise InvalidError("Current module doesn't have a run method.")

    @module_required
    @enforce_kwarg_count(0)
    @check_missing_options
    def command_check(self):
        """ Execute the `check` method of the currently loaded module """

        # Run the module if `check` method exists
        if hasattr(Module.module, "check"):
            Module.module.check()
            return

        # Otherwise raise error
        raise InvalidError("Current module doesn't have a check method.")

    @module_required
    def command_info(self) -> None:
        """Display module metadata """

        def display_info(key: str, value: str | list[str]):
            """ Display the information given """

            # If the metadata value is a list
            if isinstance(value, list):
                printf(" "*2, f"{key}:")

                # Prints the contents
                for content in value:
                    if key.lower() == "description":
                        printf(" "*4, f"{content}")
                    else:
                        printf(" "*4, f"-> {content}")

                # Add an extra line for readability after a block of list items
                printf()

            # If the metadata value is a single string or scalar
            else:
                printf(" "*2, f"{key[:15].ljust(15)} : {value}")

        # Iterate through all metadata items of the currently loaded module
        printf()
        printf("Module information")
        printf("==================")
        printf()
        for key, value in Module.module.info.items():
            display_info(key, value)

        # Display payload information if there is currently loaded
        if Module.payload:
            printf("\n")
            printf("Payload Information")
            printf("===================")
            printf()
            for key, value in Module.payload.info.items():
                display_info(key, value)

        # Display encoder information if there is currently loaded
        if Module.encoder:
            printf("Encoder Information")
            printf("===================")
            printf()
            for key, value in Module.encoder.info.items():
                display_info(key, value)

        # Prints newline
        printf()

    # --- Jobs Command Category ---

    @enforce_kwarg_count(0)
    def command_list(self):
        """ List all currently active jobs """

        # Exit if no jobs exist
        if not Session.sessions:
            print_status("There are no currently active jobs.")
            return

        # Prepare job IDs and addresses
        sn_id = [str(count) for count in range(1, len(Session.sessions) + 1)]
        sn_addr = [str((sess[1], sess[2])) for sess in Session.sessions]

        # Display active jobs in a table
        printf("\n" + "Active Jobs:" + "\n")
        print_basic_table(
            col1_header="Id",
            col2_header="Address",
            col1=sn_id,
            col2=sn_addr
        )

        # Show interaction instructions
        printf(
            "\n"
            "Interact with a job by its \"ID\" using the interact command."
            "\n"
        )

    @enforce_kwarg_count(1)
    def command_interact(self, **kwargs: Any):
        """ Interact with a specific job by its ID """
        sn_id = kwargs["arg1"]

        # Exit if no jobs exist
        if not Session.sessions:
            print_status("There are no currently active jobs.")
            return

        # Validate job ID
        IDs = [str(count) for count in range(1, len(Session.sessions) + 1)]
        if sn_id not in IDs:
            raise TypeError("Session id does not exist.")

        # Show interaction message
        print_status(
            "Interacting with... "
            f"{Session.sessions[int(sn_id) - 1][1][0]}:"
            f"{Session.sessions[int(sn_id) - 1][1][1]}\n"
        )

        # Start exploit session handler
        exploit_session = Module.payload.info["Session"]
        exploit_session(Session.sessions[int(sn_id) - 1][0])

    @enforce_kwarg_count(1)
    def command_kill(self, **kwargs: Any):
        """ Kill all jobs or a specific job by its ID """
        sn_id = kwargs["arg1"]

        # Exit if no jobs exist
        if not Session.sessions:
            print_status("There are no currently active jobs.")
            return

        # Terminate all jobs if "all" is specified
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

        # Validate job ID
        IDs = [str(count) for count in range(1, len(Session.sessions) + 1)]
        if sn_id not in IDs:
            raise TypeError("Session id does not exist.")

        # Terminate a specific job
        print_status(f"Terminating job id {sn_id}...")
        sn_count = len(Session.sessions)

        # Shutdown and close the socket of the session
        Session.sessions[int(sn_id) - 1][0].shutdown(socket.SHUT_RDWR)
        Session.sessions[int(sn_id) - 1][0].close()

        # Wait until session count decreases
        while len(Session.sessions) == sn_count:
            time.sleep(0.5)

        print_status(f"Job id {sn_id} has been terminated.")
