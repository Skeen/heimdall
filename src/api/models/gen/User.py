# pylint: disable=W9903
"""Data generator."""
import random

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from api.models.gen import util


def gen_user(boy=None, password=None):
    """Generate a randomized user account."""
    username = get_random_string(10, util.CHARACTERS)
    if password is None:
        password = "heimdall"

    user = get_user_model()(
        username=username,
        is_active=True,
        email=username + '@example.com',
    )
    user.set_password(password)

    if boy is None:
        boy = random.choice([True, False])

    if boy:
        user.first_name = random.choice(util.MALE_FIRST_NAMES)
    else:
        user.first_name = random.choice(util.FEMALE_FIRST_NAMES)
    user.last_name = random.choice(util.LAST_NAMES)
    user.full_clean()
    user.save()
    return user
