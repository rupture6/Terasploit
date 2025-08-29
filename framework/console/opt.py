# -*- coding: utf-8 -*-

# Python lib
from dataclasses import dataclass, field
from typing import Any, Callable

# Console lib
from src.utils.validator import Validate


@dataclass
class Option:
    """Base class for encapsulating option metadata."""

    name: str
    required: str
    description: str
    default: Any
    validator: Callable[[Any], bool] = field(repr=False)


@dataclass
class Boolean(Option):
    """Boolean option encapsulation."""

    def __init__(
        self,
        name: str,
        required: str,
        description: str,
        default: Any
    ) -> None:
        super().__init__(
            name, required, description, default, Validate.boolean
        )


@dataclass
class Int(Option):
    """Integer option encapsulation."""

    def __init__(
        self,
        name: str,
        required: str,
        description: str,
        default: Any
    ) -> None:
        super().__init__(
            name, required, description, default, Validate.int_object
        )


@dataclass
class Float(Option):
    """Float option encapsulation."""

    def __init__(
        self,
        name: str,
        required: str,
        description: str,
        default: Any
    ) -> None:
        super().__init__(
            name, required, description, default, Validate.float_object
        )
