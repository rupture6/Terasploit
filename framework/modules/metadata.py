# -*- coding: utf-8 -*-

# Python lib
from enum import Enum


class Extension(str, Enum):
    """Supported file extensions."""
    PHP = ".php"
    PYTHON = ".py"
    PERL = ".pl"


class Arch(str, Enum):
    """Supported architectures."""
    MULTI = "multi"
    PYTHON = "python"
    PERL = "perl"
    X86 = "x86"
    X64 = "x64"
    PHP = "php"
    CMD = "cmd"


class Platform(str, Enum):
    """Supported platforms."""
    MULTI = "multi"
    WINDOWS = "windows"
    PYTHON = "python"
    LINUX = "linux"
    PERL = "perl"
    UNIX = "unix"
    PHP = "php"
    CMD = "cmd"
    OSX = "osx"


class PayloadHandler(str, Enum):
    """Supported payload handlers."""
    REVERSE_TCP = "reverse_tcp"
    BIND_TCP = "bind_tcp"


class Module(str, Enum):
    """Supported module types."""
    AUXILIARY = "auxiliary"
    ENCODER = "encoder"
    EXPLOIT = "exploit"
    PAYLOAD = "payload"
