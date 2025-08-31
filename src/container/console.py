# -*- coding: utf-8 -*-

# Python lib
from typing import Any

# The default console settings are stored here and
# can only be modified by editing the source code.


class Setting:
    """Stores the console's default settings."""

    # Console logging settings.
    logging: bool = True
    log_level: str = "INFO"

    # Console verbosity setting.
    verbose: bool = True

    # Prompt character setting.
    prompt_char: str = ">"
    prompt_user: str = "tsf"


# Logging instance
class Logging:
    """Stores the logging instance."""
    instance: Any = None
