# -*- coding: utf-8 -*-

# Python library
import os
import random
import string
from typing import Any

# Library
from lib.utils.printer import print_status
from lib.container.module import Module

# Framework
from framework.console.options import OptGet


class Payload:
    """ Utility functions of payload module """

    # Obfuscation PHP opening tag
    PHP_START = "/*<?php /**/"

    def opt(self, key: str):
        """ Access the option dictionary to get a specific value """
        return OptGet(key)

    def generate_random_string(self, length: int = 10) -> str:
        """ Generate random strings, good for generating shell names """

        chars: list[Any] = []

        # Generate random characters
        for _ in range(length):
            chars.append(random.choice(string.ascii_letters + string.digits))

        # Return the crafted random chars string
        return "".join(chars)

    def check_bad_chars(self, payload: bytes, badchars: bytes) -> list[Any]:
        """ Return a list of badchars found in payload """
        return [b for b in badchars if b in payload]

    def encode(self, content: Any) -> Any:
        """ Encodes the given content (eg. generated payload) """

        # Check if there is a loaded encoder
        if Module.encoder:
            encoded, result = Module.encoder.encode(content)

            # Check if the result of encoding is successful
            if result is True:
                return encoded
            else:
                return content

        # Return the content if there is no encoder loaded
        return content

    def generate_payload(
        self,
        raw_payload: Any,
        binary: bool = False,
        badchars: bytes | None = None,
    ) -> dict[str, Any]:
        """ Generate a payload with encoding and badchar detection """

        # Normalize payload type
        if binary and isinstance(raw_payload, str):
            payload: Any = raw_payload.encode("utf-8")
        elif not binary and isinstance(raw_payload, bytes):
            payload = raw_payload.decode("utf-8")
        else:
            payload = raw_payload

        # Badchar detection
        if badchars and isinstance(payload, (bytes, bytearray)):
            found_badchars = self.check_bad_chars(payload, badchars)

            if found_badchars:
                if not getattr(self, "encoder", None):
                    raise ValueError(
                        f"Payload contains badchar(s): {found_badchars}"
                    )

                payload = self.encode(payload)
                if not isinstance(payload, bytes):
                    payload = payload.encode("utf-8")

                found_badchars = self.check_bad_chars(payload, badchars)
                if found_badchars:
                    raise ValueError(
                        "Badchar(s) remain even after encoding: "
                        f"{found_badchars}"
                    )

        # Final normalization
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8", errors="ignore")

        return {
            "OriginalSize": len(
                raw_payload
                if isinstance(raw_payload, (bytes, bytearray))
                else str(raw_payload).encode("utf-8")
            ),
            "FinaLSize": len(payload),
            "BadcharsChecked": bool(badchars),
            "Payload": payload,
        }

    def generate_file(
        self,
        content: Any,
        directory: str = ".",
        name: str = "payload",
        extension: str = "",
        binary: bool = False
    ) -> None:
        """ Generate a file containing the given payload content """

        # Ensure the target directory exists
        os.makedirs(directory, exist_ok=True)

        # Build the initial filename
        filename = os.path.join(directory, f"{name}{extension}")

        # If the file already exists, append a random string
        if os.path.exists(filename):
            rand = self.generate_random_string(5)
            filename = os.path.join(directory, f"{name}_{rand}{extension}")

        # Get the absolute path for clarity
        filepath = os.path.abspath(filename)

        # Normalize payload type based on binary mode
        if binary:
            if isinstance(content, str):
                content = content.encode("utf-8")
        else:
            if isinstance(content, bytes):
                content = content.decode("utf-8")

        # Choose file mode: binary write ("wb") or text write ("w")
        mode = "wb" if binary else "w"

        # Write the content to disk
        with open(filepath, mode) as f:
            f.write(content)

        # Notify where the file was saved
        print_status(f"Saved as: {filepath}")
