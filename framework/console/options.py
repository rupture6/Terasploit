# -*- coding: utf-8 -*-

# Python library
from typing import Any
from dataclasses import dataclass, field

# Library
from lib.utils.validator import Validate


@dataclass
class Opt:
    """Stores and manages module options."""

    # Stores selected exploit target
    exploit_target: dict[Any, Any] = field(
        default_factory=lambda: {"0": "Automatic Target"}
    )

    # Stores selected auxiliary mode
    auxiliary_mode: dict[Any, Any] = field(
        default_factory=dict[Any, Any]
    )

    # Stores registered module/payload options
    registered_module_options: list[Any] = field(default_factory=list[Any])
    registered_payload_options: list[Any] = field(default_factory=list[Any])

    default_options: dict[str, Any] = field(
        default_factory=lambda: {
            "URL": None,
            "RHOST": None,
            "RPORT": 80,
            "PROXY": None,
            "SSL_VERIFY": False,
            "RANDOM_AGENT": False,
            "VERBOSE": True,
            "LHOST": None,
            "LPORT": 4444,
            "TIMEOUT": None,
        }
    )

    required: dict[str, str] = field(
        default_factory=lambda: {
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
        }
    )

    description: dict[str, str] = field(
        default_factory=lambda: {
            "URL": "The target URL",
            "RHOST": "The target remote address",
            "RPORT": "The target remote port (tcp)",
            "PROXY": (
                "Json file containing proxy, "
                "e.g. {\"protocol\": \"host\", ...}"
            ),
            "SSL": "Verifies SSL certificates for HTTP requests",
            "RANDOM_AGENT": "Use a random user agent",
            "VERBOSE": "Enable verbose output for debugging",
            "LHOST": "The listen address",
            "LPORT": "The listen port (tcp)",
            "TIMEOUT": "Connection time limit",
        }
    )

    validator: dict[str, object] = field(
        default_factory=lambda: {
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
        }
    )

    options: dict[str, Any] = field(init=False)

    def __post_init__(self) -> None:
        self.reset_to_default()

    @staticmethod
    def format_value(value: Any) -> Any:
        """Convert a string into bool, int, or float when possible."""
        if not isinstance(value, str):
            return value

        txt = value.strip().lower()

        if txt in {"true", "false"}:
            return txt == "true"

        for cast in (int, float):
            try:
                return cast(txt)
            except ValueError:
                continue

        return value

    @classmethod
    def clear_mode(cls) -> None:
        """Clear auxiliary mode."""
        cls.auxiliary_mode.clear()

    @classmethod
    def clear_target(cls) -> None:
        """Clear exploit target."""
        cls.exploit_target.clear()

    @classmethod
    def reset_to_default(cls) -> None:
        """Restore all options and metadata to defaults."""

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
        cls.required = cls.required.copy()
        cls.description = cls.description.copy()
        cls.validator = cls.validator.copy()


def get_option_value(key: str = "") -> Any:
    """Access stored option(s). Keys must be uppercase."""
    return Opt.options if not key else Opt.options.get(key.upper())
