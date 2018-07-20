#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W9903
# pylint: disable=undefined-variable
# flake8: noqa: F821
"""Tool for generating test data."""
import argparse
import os
import random
from contextlib import contextmanager

from django.db import transaction

def load_or_default(varname, default):
    """Set variable :code:`varname`.

    Will be set to the corresponding environment variable value if any such
    one exists, otherwise it will be set to the provided default value.
    """
    value = os.environ[varname] if varname in os.environ else default
    globals()[varname] = int(value)
    # print varname + "=" + value


load_or_default('USERS', 20)
load_or_default('PUBLIC_KEYS_PER_USER_MIN', 0)
load_or_default('PUBLIC_KEYS_PER_USER_MAX', 3)

load_or_default('GROUPS', 5)
load_or_default('USERS_PER_GROUP_MIN', 0)
load_or_default('USERS_PER_GROUP_MAX', 5)
load_or_default('KEYENTRIES', 5)


def get_random_row(collection):
    """Get a random row / object from the provided collection."""
    from random import randint

    count = collection.objects.count()
    random_index = randint(0, count - 1)
    return collection.objects.all()[random_index]


@contextmanager
def step(command):
    """Format the output for running steps of the script.

    Writes :code:`command` followed by running the function, then 'OK' with
    elapsed running time, before returning.
    """
    import sys
    import time

    sys.stdout.write(command + "...")
    sys.stdout.flush()
    start = time.time()
    yield
    end = time.time()
    run_time = (end - start)
    sys.stdout.write("OK (" + format(run_time, '.1f') + "s)" + "\n")
    sys.stdout.flush()


def main():
    """Populate db according to arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--gendata',
        help='Generate randomized applicant and building data.',
        dest='gen_data',
        action='store_true',
        default=False
    )
    args = parser.parse_args()

    with step("Setup Django"):
        import django

        # Setup django
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "heimdall.testing_settings"
        )
        django.setup()

    if args.gen_data:
        with transaction.atomic(savepoint=True):
            gen_random_data()


# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def gen_random_data():
    """Insert randomly generated data in the database."""

    print "Heimdall data generator"
    print "Running takes ~3 minutes..."
    print ""

    with step("Generate users"):
        from django.contrib.auth import get_user_model
        from api.models.gen import gen_user
        from api.models.gen import gen_public_key

        assert USERS >= 0
        assert PUBLIC_KEYS_PER_USER_MIN >= 0

        while get_user_model().objects.count() < USERS:
            user = gen_user()

            num_public_keys = random.randint(
                PUBLIC_KEYS_PER_USER_MIN,
                PUBLIC_KEYS_PER_USER_MAX
            )
            for _ in range(num_public_keys):
                gen_public_key(user=user)

    with step("Generate groups"):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from api.models.gen import gen_group

        assert GROUPS >= 0
        assert USERS_PER_GROUP_MIN >= 0
        assert USERS_PER_GROUP_MAX < USERS

        while Group.objects.count() < GROUPS:
            group = gen_group()

            num_members = random.randint(
                USERS_PER_GROUP_MIN,
                USERS_PER_GROUP_MAX,
            )
            while get_user_model().objects.filter(groups=group).count() < num_members:
                user = get_random_row(get_user_model())
                group.user_set.add(user)

    # -- Generate application targets
    with step("Generate key entries"):
        from api.models import KeyEntry
        from api.models.gen import gen_key_entry

        while KeyEntry.objects.count() < KEYENTRIES:
            key_entry = gen_key_entry()


if __name__ == "__main__":
    # Ignore all warnings, we want our output clear
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
