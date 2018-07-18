#!/usr/bin/env python
"""Inspects the source tree, as specified by `.coveragerc` and prints files."""
import argparse
import os


def find_files(extensions, src_dir):
    """Produce a list of files of interest.

    Args:
        extensions (:obj:`list` of :obj:`str`):
            A list of file extensions to look for.

        src_dir (:obj:`str`):
            The directory to start the recursive search in.

    Yields:
        str: A list of files found within `src_dir`, with one of the given
            `extensions`.
    """
    for (dirpath, _, filenames) in os.walk(src_dir):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in extensions:
                yield os.path.join(dirpath, filename)


def main():
    """Print files yielded by find_files."""
    parser = argparse.ArgumentParser()
    # pylint: disable=W9903
    parser.add_argument('extensions', nargs='+')
    parser.add_argument('--paths', dest='paths', nargs='+')
    args = parser.parse_args()

    paths = ['.']
    if args.paths:
        paths = args.paths

    for path in paths:
        for src in find_files(tuple(args.extensions), path):
            print src


if __name__ == "__main__":
    main()
