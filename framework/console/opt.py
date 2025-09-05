# -*- coding: utf-8 -*-

# Python library
from dataclasses import dataclass
from typing import Any

# Library
from lib.utils.validator import Validate


@dataclass(init=True)
class Option:
    """ Base option encapsulation """

    name: str
    required: str
    description: str
    default: Any
    validator: Any = None


@dataclass(init=True)
class Boolean:
    """ Boolean option encapsulation """

    name: str
    required: str
    description: str
    default: Any
    validator = Validate.boolean


@dataclass(init=True)
class Int:
    """ Int option encapsulation """

    name: str
    required: str
    description: str
    default: Any
    validator = Validate.int_object


@dataclass(init=True)
class Float:
    """ Float option encapsulation """

    name: str
    required: str
    description: str
    default: Any
    validator = Validate.float_object
