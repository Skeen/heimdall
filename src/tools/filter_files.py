#!/usr/bin/env python
"""Filter a list of files from stdin.

Utilizes coverage.py_ matchers for filtering.

.. _coverage.py: https://coverage.readthedocs.io/en/coverage-4.3.4/
"""

import sys
from coverage.files import FnmatchMatcher
from coverage.files import prep_patterns


def filter_files(omit):
    """Read files from stdin, filter and yield passing ones."""
    omit = prep_patterns(omit)
    omit_match = FnmatchMatcher(omit)

    while True:
        # Read filenames
        src = sys.stdin.readline()
        if src == '':
            break

        if omit_match.match(src):
            continue
        yield src.rstrip()


def main():
    """Print the yielded filtered files. Flushing after each line."""
    omit = sys.argv[1:]
    if len(omit) == 0:
        omit = ['']

    for src in filter_files(omit):
        sys.stdout.write(src + '\n')
        sys.stdout.flush()


if __name__ == "__main__":
    main()
