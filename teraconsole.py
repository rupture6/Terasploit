#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import sys

    if sys.argv[1:]:
        pass

    # Start command line interface if no argv is specified.
    else:
        pass

except KeyboardInterrupt:
    print("Interrupt signal... console terminated.")
    sys.exit(130)
