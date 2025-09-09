# -*- coding: utf-8 -*-

# Library
from lib.utils.printer import printf
from lib.utils.path import module_list

# Framework
from framework.metadata import (
    version,
    copyright,
    email
)

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

    # Terasploit framework
    printf("\033[33m", f"Terasploit Framework {version}", "\033[0m")

    # Display copyright and email
    printf("", f"{copyright} {email}", "\n")

    # Display the module count
    printf("", f"Modules: ({len(module_list())})")

    # Display the counts of each module category
    printf("", module_count + "\n"*2)
