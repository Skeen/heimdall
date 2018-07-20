# pylint: disable=W9903
"""Utilities for data generators."""

import os
import random
from datetime import timedelta
from django.conf import settings


def read(filename, strip=True):
    """Read 'filename' as unicode, and return a tuple of strings."""
    import codecs
    lines = tuple(codecs.open(filename, encoding='utf-8', mode='r'))
    if strip is False:
        return lines
    return [s.strip() for s in lines]


# Relative path to the resources folder
RES_FOLDER = settings.BASE_DIR + "/api/models/gen/res/"

# Files
# -----
BIRDS_FILE = os.path.join(
    os.path.dirname(__file__),
    RES_FOLDER + 'danske_fugle'
)
BIRDS = read(BIRDS_FILE)

FEMALE_FIRST_NAMES_FILE = os.path.join(
    os.path.dirname(__file__),
    RES_FOLDER + 'fornavne_piger'
)
FEMALE_FIRST_NAMES = read(FEMALE_FIRST_NAMES_FILE)

MALE_FIRST_NAMES_FILE = os.path.join(
    os.path.dirname(__file__),
    RES_FOLDER + 'fornavne_drenge'
)
MALE_FIRST_NAMES = read(MALE_FIRST_NAMES_FILE)

LAST_NAMES_FILE = os.path.join(
    os.path.dirname(__file__),
    RES_FOLDER + 'efternavne'
)
LAST_NAMES = read(LAST_NAMES_FILE)


CHARACTERS = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'


def random_time(start, end):
    """Generate a random time between start and end."""
    return start + timedelta(
        seconds=random.randint(
            0,
            int((end - start).total_seconds())
        )
    )


def random_date(start, end):
    """Generate a random date between start and end."""
    return random_time(start, end).date()
