# pylint: disable=W9903
"""Data generator."""
import random

from django.utils.crypto import get_random_string

from api.models import KeyEntry

from api.models.gen import util
from api.models.gen import gen_group


def gen_key_entry(owner=None):
    """Generate a randomized key_entry."""
    if owner is None:
        owner = gen_group()

    bird = random.choice(util.BIRDS)  
    title = "Login til " + bird + " systemet"
    username = get_random_string(10, util.CHARACTERS)
    url = 'magenta.dk'
    notes = ''

    key_entry = KeyEntry(
        owner=owner,
        title=title,
        username=username,
        url=url,
        notes=notes,
    )
    key_entry.full_clean()
    key_entry.save()
    return key_entry
