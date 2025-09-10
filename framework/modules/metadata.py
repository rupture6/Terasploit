# -*- coding: utf-8 -*-

# Python library
import json
import os

# Absolute path of the main directory
PATH = str(os.path.abspath(os.getcwd())) + "/db/module-metadata.json"

# Module metadata json file
with open(PATH, "r", encoding="utf-8") as metadata_file:
    metadata_ = json.load(metadata_file)


class Extension:
    """ Supported file extensions """

    PHP = ".php"
    PYTHON = ".py"
    PERL = ".pl"


class Arch:
    """ Supported architectures """

    MULTI = "multi"
    PYTHON = "python"
    PERL = "perl"
    X86 = "x86"
    X64 = "x64"
    PHP = "php"
    CMD = "cmd"


class Platform:
    """ Supported platforms """

    MULTI = "multi"
    WINDOWS = "windows"
    PYTHON = "python"
    LINUX = "linux"
    PERL = "perl"
    UNIX = "unix"
    PHP = "php"
    CMD = "cmd"
    OSX = "osx"


class PayloadHandler:
    """ Supported payload handlers """

    REVERSE_TCP = "reverse_tcp"
    BIND_TCP = "bind_tcp"


class Module:
    """ Supported module types """

    AUXILIARY = "auxiliary"
    ENCODER = "encoder"
    EXPLOIT = "exploit"
    PAYLOAD = "payload"
