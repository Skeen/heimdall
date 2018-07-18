#!/usr/bin/env python
# pylint: disable=W9903
"""Tool for cleaning up duplicates in django.po files."""
import sys

if __name__ == "__main__":
    # pylint: disable=invalid-name
    argv = sys.argv
    # pylint: disable=invalid-name
    translation_file = argv[1] if len(argv) > 1 else None

    lines = []
    msgids = []
    reading_msgid = False
    msgid = ""
    skip = False

    # Read input file, line by line
    with open(translation_file) as f:
        for line in f:
            # If we see a msgid, start reading it, until we see a msgstr tag.
            # At which point we know the msgid is complete.
            if line.startswith("msgid"):
                reading_msgid = True
            if reading_msgid:
                if line.startswith("msgstr"):
                    # Once the entire msgid tag is read, stop reading anymore.
                    reading_msgid = False
                    # Check if we've seen it already (i.e. if it's a duplicate)
                    skip = bool(msgid in msgids)
                    # Add the msgid to the know msgids
                    msgids.append(msgid)
                    msgid = ""
                else:
                    msgid += line

            # When we've read an entire translation block there will be space.
            if line in ['\n', '\r\n']:
                # If the current block is a duplicate, discard it.
                # If it is not, print it.
                if skip is False:
                    for line in lines:
                        print line.strip()
                    print ""
                lines = []
            else:
                lines.append(line)
