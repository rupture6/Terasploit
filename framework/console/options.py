# -*- coding: utf-8 -*-

# Python lib
from typing import Any
from dataclasses import dataclass, field

# Lib
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
        self.reset_to_defaults()

    @staticmethod
    def format_value(value: Any) -> Any:
        """Convert string input into bool/int/float when possible."""
        if isinstance(value, str):
            val = value.strip().lower()
            if val in {"true", "false"}:
                return val == "true"
            for cast in (int, float):
                try:
                    return cast(value)
                except ValueError:
                    pass
        return value

    def clear_mode(self) -> None:
        """Clear auxiliary mode."""
        self.auxiliary_mode.clear()

    def clear_target(self) -> None:
        """Clear exploit target."""
        self.exploit_target.clear()

    def reset_to_defaults(self) -> None:
        """Restore all options and metadata to defaults."""
        self.options = self.default_options.copy()
        self.registered_module_options.clear()
        self.registered_payload_options.clear()

        # Reset metadata copies
        self.required = self.required.copy()
        self.description = self.description.copy()
        self.validator = self.validator.copy()


def get_option_value(opt: Opt, key: str = "") -> Any:
    """Access stored option(s). Keys must be uppercase."""
    return opt.options if not key else opt.options.get(key.upper())
