# -*- coding: utf-8 -*-

# Python lib
from typing import Any, cast


class Module:
    """Class for storing and managing references to other classes."""

    # The main module that is currently in use is stored here.
    module = cast(Any, None)
    module_path = cast(Any, None)

    # The payload of exploit module is stored in here.
    payload = cast(Any, None)
    payload_path = cast(Any, None)

    # The encoder of exploit module is stored in here.
    encoder = cast(Any, None)
    encoder_path = cast(Any, None)
