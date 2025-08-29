# -*- coding: utf-8 -*-

# The default console settings are stored here and
# can only be modified by editing the source code.


class Setting:
    """Stores the console's default settings."""

    # Console logging settings.
    logging: bool = False
    log_level: int = 0

    # Console verbosity setting.
    verbose: bool = True

    # Prompt character setting.
    prompt_char: str = ">"
    prompt_user: str = "tsf"
