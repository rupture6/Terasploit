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

ascii_art = """
┌───────────────────────────────────────────────┐
│ root@parrot:~# ./exploit target=10.0.0.5      │
│                                               │
│ \033[93m[*]\033[0m Connecting to 10.0.0.5:22 ...             │
│ \033[93m[*]\033[0m Sending payload ...                       │
│ \033[93m[*]\033[0m Waiting for response ...                  │
│                                               │
│ \033[91m!!! ERROR !!!\033[0m                                 │
│ \033[91mConnection reset by peer (code: 1337)\033[0m         │
│                                               │
│ \033[93m[!]\033[0m Exploit failed. Target might be patched.  │
│                                               │
│ root@parrot:~# _                              │
└───────────────────────────────────────────────┘
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
        "\n\n"
    )
