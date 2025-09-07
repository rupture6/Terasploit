# -*- coding: utf-8 -*-

# Python library
from typing import cast, Any


class Module:
    """Class for storing and managing references to other classes."""

    # Main module currently in use
    module = cast(Any, None)
    module_path = cast(Any, None)

    # Exploit payload
    payload = cast(Any, None)
    payload_path = cast(Any, None)

    # Exploit encoder
    encoder = cast(Any, None)
    encoder_path = cast(Any, None)
