# pylint: disable=W9903
"""Data generator."""
import random

from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string

from api.models.gen import util


def gen_group(name=None):
    """Generate a randomized group."""
    if name is None:
        name = get_random_string(10, util.CHARACTERS)
    group = Group(
        name=name
    )
    group.full_clean()
    group.save()
    return group
