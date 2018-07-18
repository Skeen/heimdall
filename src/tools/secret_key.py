#!/usr/bin/env python
"""Tool to generate a :django:setting:`SECRET_KEY` for settings.py.

The key is printed to `stdout`.

Used by: :ref:`tools/gen_settings.sh`
"""

from django.utils.crypto import get_random_string

# pylint: disable=W9903
VALID_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
"""The list of valid characters for a secret key."""


def gen_secret_key(length=50):
    """Generate a secret key.

    Args:
        length (int): Length of the key to generate.

    Returns:
        str: The generated key
    """
    return get_random_string(length, VALID_CHARACTERS)


if __name__ == "__main__":
    print gen_secret_key()
