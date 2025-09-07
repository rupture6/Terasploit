# -*- coding: utf-8 -*-

# Python library
import os
import sys


def module_list() -> list[str]:
    """ Return paths of all Python modules in the 'modules' directory """
    base_dir = os.path.join(sys.path[0], "modules")
    module_paths: list[str] = []

    for root, dirs, _ in os.walk(base_dir):
        for subdir in dirs:
            for file in os.listdir(os.path.join(root, subdir)):

                if file.endswith(".py") and file != "__init__.py":
                    _path = os.path.relpath(
                        os.path.join(os.path.join(root, subdir)),
                        base_dir,
                    )

                    module = _path.replace(os.sep, "/") + f"/{file}"
                    module_paths.append(module.removesuffix(".py"))

    return sorted(module_paths)


def search_modules(module_name: str) -> list[str]:
    """ Return a list of module paths matching the given string """
    return sorted([m for m in module_list() if module_name in m])


def humanize_path(module_path: str) -> str:
    """ Convert a Python import path to a normal filesystem path """
    return module_path.replace(".", os.sep)


def parse_human_path(human_path: str) -> list[str]:
    """ Split a human-readable filesystem path into parts """
    return [part for part in human_path.split(os.sep) if part]


def parse_python_path(path: str) -> list[str]:
    """ Split a Python import path into parts """
    return [part for part in path.split(".") if part]


def join_path_list(path_list: list[str], path_type: str = "pythonize") -> str:
    """ Join a list of path elements into a single string """
    if path_type == "pythonize":
        return ".".join(path_list)
    if path_type == "humanize":
        return os.sep.join(path_list)

    raise ValueError(f"Invalid path type: {path_type}")


def modulize_path(path: str) -> str:
    """ Convert a filesystem path into a Python importable path """
    segments = parse_human_path(path)
    if not segments or segments[0] not in {"modules", "module"}:
        segments.insert(0, "modules")
    else:
        segments[0] = "modules"

    return join_path_list(segments, path_type="pythonize")
