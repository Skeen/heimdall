#!/usr/bin/env python
# pylint: disable=W9903
"""Tool for pretty printing test runs."""
import fileinput
import sys

if __name__ == "__main__":

    # pylint: disable=invalid-name
    test_name = None

    # Read input stream, line by line
    for line in fileinput.input():
        if line.startswith("test_"):
            test_name = line.split()[0]
            test_name = ((test_name[:50] + '...')
                         if len(test_name) > 75
                         else test_name)
        if test_name is not None:
            if " ... ok" in line:
                print test_name, 0
            if " ... FAIL" in line:
                print test_name, 1
            sys.stdout.flush()
