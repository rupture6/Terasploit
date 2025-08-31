# -*- coding: utf-8 -*-

# Src
from src.utils.printer import printf
from src.utils.path import module_list

# Framework
from framework.metadata import (
    version,
    github,
    copyright
)

ascii_art = """
  _____              _____       _       _ _
 |_   _|            /  ___|     | |     (_) |
   | | ___ _ __ __ _\\ `--. _ __ | | ___  _| |_
   | |/ _ \\ '__/ _` |`--. \\ '_ \\| |/ _ \\| | __|
   | |  __/ | | (_| /\\__/ / |_) | | (_) | | |_
   \\_/\\___|_|  \\__,_\\____/| .__/|_|\\___/|_|\\__|
             Exploitation | | Framework
                          |_|
"""

categories = ["auxiliary", "exploit", "encoder", "payload"]
modules: dict[str, int] = {cat: 0 for cat in categories}

for module in module_list():
    for cat in categories:
        if cat in module:
            modules[cat] += 1


def display_banner() -> None:
    """Display the banner of the Terasploit framework."""

    # Create the module count string
    module_count = ", ".join(
        f"{cat}: {count}" for cat, count in modules.items()
    )

    printf(
        # Display the ASCII art banner
        ascii_art,
        "\n\x1b[33m"
        f"Terasploit Framework {version} (CLI)"
        "\x1b[0m\n\n",

        # Display the copyright
        copyright,
        "\n",

        # Display the GitHub
        github,
        "\n\n",

        # Display the module count
        " "*2, f"{module_count}",
        "\n"
    )
