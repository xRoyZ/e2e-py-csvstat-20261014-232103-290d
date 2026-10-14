"""Ermöglicht ``python -m csvstat`` und delegiert an :func:`csvstat.cli.main`."""

import sys

from csvstat.cli import main

if __name__ == "__main__":
    sys.exit(main())
