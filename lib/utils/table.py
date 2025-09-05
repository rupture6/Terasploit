# -*- coding: utf-8 -*-
"""Terasploit UI Tables."""

# Python library
from typing import Sequence
from textwrap import wrap

# Framework
from framework.modules.metadata import metadata_

# Library
from lib.utils.printer import printf, print_error


def underline(text: str) -> str:
    """ Return dashes matching the length of `text` """
    return "-" * len(text)


def highlight(text: str, term: str, color: str = "\x1b[1;31m") -> str:
    """ Return `text` with `term` highlighted using ANSI colors """
    return text.replace(term, f"{color}{term}\x1b[0m") if term else text


def wrap_text(text: str, width: int) -> list[str]:
    """ Wrap text to a list of lines with given width """
    return wrap(text, width=width) or [""]


def print_module_path_table(
    path: Sequence[str],
    highlight_term: str = ""
) -> None:
    """ Print a table of module paths and descriptions """

    # Check if path is empty
    if not path:
        print_error("No modules found.")
        return

    col1_w = len(max(path, key=len)) + 3
    col2_w = 60

    # Header
    printf(
        "   "
        f"{'Module Path'.ljust(col1_w)}"
        " "
        "Description"
    )
    printf(
        "   "
        f"{underline('Module Path').ljust(col1_w)}"
        " "
        f"{underline('Description')}"
    )

    # Rows
    for module_path in path:
        key = next(
            (k for k in ("exploit", "auxiliary", "encoder", "payload")
             if k in module_path),
            None,
        )
        desc = (
            metadata_.get(key, {}).get(module_path, {}).get("Description", "")
        )
        for i, line in enumerate(wrap_text(desc, col2_w)):
            left = module_path.ljust(col1_w) if i == 0 else " " * col1_w
            printf(
                highlight(
                    "   "
                    f"{left} {line}",
                    highlight_term
                )
            )

        if key == "exploit":
            data = metadata_[key][module_path]
            if (cve := data.get("CVE")) and cve != "N/A":
                printf(
                    "      "
                    f"\\_ CVE: {cve}"
                )
            if (disclosure := data.get("Disclosure")) and disclosure != "N/A":
                printf(
                    "      "
                    f"\\_ Disclosure: {disclosure}"
                )
    # Footer
    printf("\n")


def print_basic_table(
    col1: Sequence[str],
    col2: Sequence[str],
    col1_width: int = 0,
    pad: int = 3,
    col1_header: str = "Name",
    col2_header: str = "Description",
    highlight_term: str = "",
) -> None:
    """ Print a two-column table with headers and wrapping """
    col1_w = col1_width or len(max(col1, key=len)) + pad
    col2_w = 60

    printf(
        "   "
        f"{col1_header.ljust(col1_w)}"
        " "
        f"{col2_header}"
    )
    printf(
        "   "
        f"{underline(col1_header).ljust(col1_w)}"
        " "
        f"{underline(col2_header)}"
    )

    for k, d in zip(col1, col2):
        for i, line in enumerate(wrap_text(d, col2_w)):
            left = k.ljust(col1_w) if i == 0 else " " * col1_w
            printf(highlight(f"   {left} {line}", highlight_term))

    # Footer
    printf()


def print_options_table(
    names: list[str],
    values: list[str],
    required: list[str],
    descriptions: list[str],
) -> None:
    """ Print a four-column table for module options """

    # Normalize values (replace None with empty string)
    current_settings: list[str] = [
        "" if str(setting) == str(None) else str(setting)
        for setting in values
    ]

    # Prepare headers and corresponding columns
    headers = ["Name", "Current Settings", "Required", "Description"]
    columns = [names, current_settings, required, descriptions]

    # Calculate dynamic column widths
    col_width = [
        max(len(str(item)) for item in col + [header]) + 2
        for header, col in zip(headers, columns)
    ]

    # Build and print header row
    header = "   "
    header += f"{'Name'.ljust(col_width[0])}"
    header += f"{'Current Settings'.ljust(col_width[1])}"
    header += f"{'Required'.ljust(col_width[2])}"
    header += f"{'Description'.ljust(col_width[3])}"
    printf(header)

    # Build and print header underline
    underline = "   "
    underline += f"{'-' * 4}".ljust(col_width[0])
    underline += f"{'-' * len('Current Settings')}".ljust(col_width[1])
    underline += f"{'-' * len('Required')}".ljust(col_width[2])
    underline += f"{'-' * len('Description')}".ljust(col_width[3])
    printf(underline)

    # Print each row in the options table
    for name, current, require, description in zip(
        names, current_settings, required, descriptions
    ):
        row = "   "
        row += f"{name.upper().ljust(col_width[0])}"
        row += f"{current.ljust(col_width[1])}"
        row += f"{require.ljust(col_width[2])}"
        row += description
        printf(row)

    # Print trailing newline / suffix
    printf()
