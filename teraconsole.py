#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import sys

    # Disable bytecode compilation.
    sys.dont_write_bytecode = True

    if sys.argv[1:]:
        pass

    # Start command line interface of console if
    # there is no argument vector specified.
    else:
        pass

except KeyboardInterrupt:
    print("Interrupt signal... console terminated.")
    sys.exit(130)
