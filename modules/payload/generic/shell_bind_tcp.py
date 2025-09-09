# -*- coding: utf-8 -*-

"""
Payload: Generic Shell Bind TCP
Documentation: N/A
"""

# Framework
from framework.sessions.unix import pulsar_generic
from framework.modules.metadata import (
    Module,
    Arch,
    Platform,
    PayloadHandler
)


class TerasploitModule:

    def __init__(self):
        self.info = dict(
            Name="Generic Shell Bind TCP",
            License="BSD-3-Clause License",
            Module=Module.PAYLOAD,
            Arch=Arch.MULTI,
            Platform=Platform.MULTI,
            PayloadHandler=PayloadHandler.BIND_TCP,
            Session=pulsar_generic.session,
            Author=[
                "charlie <castilloncharlie.a[a]gmail.com>"
            ],
            Description=[
                "Connect to the target machine and spawn an interactive shell."
            ],
            DefaultOptions=["RHOST", "LPORT"]
        )
