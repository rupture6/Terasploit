# -*- coding: utf-8 -*-

# Python library
from typing import Any

# Library
from lib.utils.validator import Validate


class Opt:
    """ Stores and manages module options """

    # exploit target
    exploit_target: dict[str, str] = {"0": "Automatic Target"}

    # auxiliary mode
    auxiliary_mode: dict[str, str] = {}

    # registered options
    registered_module_options: list[Any] = []
    registered_payload_options: list[Any] = []

    # The default values of options
    default: dict[str, Any] = {
        "URL": None,
        "RHOST": None,
        "RPORT": 80,
        "PROXY": None,
        "SSL": False,
        "RANDOM_AGENT": False,
        "VERBOSE": False,
        "LHOST": None,
        "LPORT": 4444,
        "TIMEOUT": None,
        "PROXYUSER": None,
        "PROXYPASS": None,
        "USERNAME": None,
        "PASSWORD": None
    }

    # The main options value storage
    options = default.copy()

    # Default options for reset, this variable remains untouched
    default_options = default.copy()

    required: dict[str, str] = {
        "URL": "yes",
        "RHOST": "yes",
        "RPORT": "yes",
        "PROXY": "no",
        "SSL": "no",
        "RANDOM_AGENT": "no",
        "VERBOSE": "no",
        "LHOST": "yes",
        "LPORT": "yes",
        "TIMEOUT": "no",
        "PROXYUSER": "yes",
        "PROXYPASS": "yes",
        "USERNAME": "yes",
        "PASSWORD": "yes"
    }

    # Default required, this variable remains unchanged.
    default_required = required.copy()

    description: dict[str, str] = {
        "URL": "The target URL",
        "RHOST": "The target remote address",
        "RPORT": "The target remote port (tcp)",
        "PROXY": "Json file containing proxy... {'protocol':'host',...}",
        "SSL": "Verifies SSL certificates for HTTP requests",
        "RANDOM_AGENT": "Use a random user agent",
        "VERBOSE": "Enable verbose output for debugging",
        "LHOST": "The listen address",
        "LPORT": "The listen port (tcp)",
        "TIMEOUT": "Connection time limit",
        "PROXYUSER": "Username for proxy authentication",
        "PROXYPASS": "Password for proxy authentication",
        "USERNAME": "Username for authentication",
        "PASSWORD": "Password for authentication"
    }

    # Default description, this variable remains unchanged.
    default_description = description.copy()

    validator: dict[str, Any] = {
        "URL": Validate.url,
        "RHOST": Validate.host,
        "RPORT": Validate.port,
        "PROXY": Validate.file_exists,
        "SSL": Validate.boolean,
        "RANDOM_AGENT": Validate.boolean,
        "VERBOSE": Validate.boolean,
        "LHOST": Validate.host,
        "LPORT": Validate.port,
        "TIMEOUT": Validate.int_float_object,
        "PROXYUSER": None,
        "PROXYPASS": None,
        "USERNAME": None,
        "PASSWORD": None
    }

    # Default validator, this variable remains unchanged.
    default_validator = validator.copy()

    @staticmethod
    def format_value(value: Any) -> Any:
        """ Formats the value into its appropriate type """
        value_str = str(value).lower()

        # Convert to boolean if applicable
        if value_str in ["true", "false"]:
            return value_str == "true"

        # Object type list
        _obj: object = [int, float]

        # Attempt to convert to int or float
        for _type in _obj:
            try:
                return _type(value)
            except ValueError:
                continue

        # Return as string if no conversion is successful
        return str(value)

    @classmethod
    def clear_mode(cls):
        """ Clears the auxiliary mode """
        cls.auxiliary_mode.clear()

    @classmethod
    def clear_target(cls):
        """ Clear the exploit target """
        cls.exploit_target.clear()

    @classmethod
    def reset_to_default(cls):
        """ Reset all options to their default values """

        # Reset all options to their default values
        for opt_list in [
            cls.registered_module_options,
            cls.registered_payload_options
        ]:
            for key in opt_list:
                if key not in cls.default_options:
                    del cls.options[key]
                    continue
                cls.options[key] = cls.default_options[key]

        # Clear registered options
        cls.registered_module_options.clear()
        cls.registered_payload_options.clear()

        # Reset metadata copies
        cls.default = cls.default_options.copy()
        cls.required = cls.default_required.copy()
        cls.description = cls.default_description.copy()
        cls.validator = cls.default_validator.copy()


def OptGet(key: str = "") -> Any:
    """ Access stored option(s). Keys must be uppercase """

    # Check for lowercase key value
    value = Opt.options.get(key)
    if value is None:

        # Check for default option value
        default_option_value = Opt.options.get(key.upper())
        if default_option_value is None:
            return None

        return default_option_value
    return value
