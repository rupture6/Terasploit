# -*- coding: utf-8 -*-

# Library
from lib.utils.printer import printf
from lib.utils.path import module_list

# Framework
from framework.metadata import (
    version,
    github,
    copyright
)

description = """
A general-purpose offensive security framework for developing,
executing, and managing exploits, payloads, and related modules.
"""

categories = ["auxiliary", "exploit", "encoder", "payload"]
modules: dict[str, int] = {cat: 0 for cat in categories}

for module in module_list():
    for cat in categories:
        if cat in module:
            modules[cat] += 1


def display_banner() -> None:
    """ Display the banner of the Terasploit framework """

    # Create the module count string
    module_count = ", ".join(
        f"{cat}: {count}" for cat, count in modules.items()
    )

    banner = "\033[33m" + f"Terasploit Framework {version} (CLI)" + "\033[0m"

    # Prints everything all at once
    printf(
        # Banner
        banner + "\n" +

        # Description
        description + "\n" +

        # Display the copyright
        copyright + "\n" +

        # Display the GitHub
        github + "\n"*2 +

        # Display the module count
        f"Modules: ({len(module_list())})" + "\n" +

        # Display the counts of each module category
        module_count + "\n"*2
    )
