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


load_or_default('APPLICANTS', 50)
load_or_default('APPLICATIONS', 250)
load_or_default('BUILDINGS', 10)
load_or_default('TENANCY_GROUPS', 10)
load_or_default('TENANCIES', 50)
load_or_default('OFFERS', 50)
load_or_default('OFFERS_SENT', 250)
load_or_default('MESSAGES', 50)


def get_random_row(collection):
    """Get a random row / object from the provided collection."""
    from random import randint

    count = collection.objects.count()
    random_index = randint(0, count - 1)
    return collection.objects.all()[random_index]


def gen_extra_ubs_admins():
    """Generate UBS admin users."""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    from django.utils import timezone
    # Additional ones
    username = "ubsadmin"
    for _ in range(0, 9):
        username += 'a'
        ubsadmin = get_user_model()(
            username=username,
            is_active=True,
            is_superuser=True,
            is_staff=True,
            email=username + "@system.com",
            first_name=username,
            last_login=timezone.now()
        )
        ubsadmin.set_password(username)
        ubsadmin.save()

        group, _ = Group.objects.get_or_create(name='ubsadmin')
        group.user_set.add(ubsadmin)
        group.save()


def get_applicants():
    """Get a randomized list of applicants, with len either 1 or 2."""
    from webapp.models import Applicant
    from random import choice

    applicants = choice([
        [get_random_row(Applicant)],
        [get_random_row(Applicant),
         get_random_row(Applicant)]
    ])
    return applicants


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
    parser.add_argument(
        '--recalc_constraints',
        help='Recalculate constraints.',
        dest='recalc_constraints',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--recalc_points',
        help='Recalculate points.',
        dest='recalc_points',
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
        # Setup test-runner and run tests
        # from webapp.models.gen import gen_offer_sent

    if args.gen_data:
        with transaction.atomic(savepoint=True):
            gen_random_data()

    if args.recalc_points:
        with transaction.atomic(savepoint=True):
            recalculate_rules()

    if args.recalc_constraints:
        with transaction.atomic(savepoint=True):
            recalculate_constraint_rules()


# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def gen_random_data():
    """Insert randomly generated data in the database."""

    print "Boligadmin data generator"
    print "Running takes ~3 minutes..."
    print ""

    # -- Generate ubsadmin account
    with step("Generating extra ubsadmin accounts"):
        gen_extra_ubs_admins()

    with step("Generate applicants"):
        from webapp.models.gen.Applicant import gen_applicant
        from webapp.models.util import APPLICANT_STATUS_HOLD

        for _ in range(1, APPLICANTS):
            gen_applicant(active_status=APPLICANT_STATUS_HOLD)

    with step("Generate educations"):
        from webapp.models import Applicant
        from webapp.models.gen.Education import gen_education
        from webapp.models.util import EDU_STATUS_IN_PROGRESS

        for applicant in Applicant.objects.all():
            gen_education(applicant, status=EDU_STATUS_IN_PROGRESS)

    # -- Generate application targets
    with step("Generate buildings"):
        from webapp.models.ApprobationCommittee import ApprobationCommittee
        from webapp.models.gen import gen_building

        for _ in range(1, BUILDINGS):
            committee = get_random_row(ApprobationCommittee)
            gen_building(app_committee=committee)

    with step("Generate tenancy groups"):
        from webapp.models import Building
        from webapp.models.gen import gen_tenancy_group
        from webapp.models import TenancyGroup

        for _ in range(1, TENANCY_GROUPS):
            building = get_random_row(Building)
            gen_tenancy_group(in_building=building)

    with step("Generate tenancies"):
        from webapp.models import TenancyGroup
        from webapp.models.gen import gen_tenancy

        for _ in range(1, TENANCIES):
            group = get_random_row(TenancyGroup)
            gen_tenancy(group=group)

    # -- Generate applications
    with step("Generate applications"):
        from webapp.models import ApplicationTarget
        from webapp.models.gen import gen_application

        for _ in range(1, APPLICATIONS):
            application_target = get_random_row(ApplicationTarget)
            gen_application(
                appl_target=application_target,
                applicants=get_applicants(),
                status_change=True,
            )

    with step("Set applicants active"):
        from webapp.models.gen.Applicant import set_applicants_active
        set_applicants_active()

    # -- Generate offers
    with step("Generate offers"):
        from webapp.models import Tenancy
        from webapp.models.gen import gen_offer

        for _ in range(1, OFFERS):
            tenancy = get_random_row(Tenancy)
            offer = gen_offer(tenancy=tenancy)

    # -- Generate send offers
    with step("Generate offers sent"):
        from webapp.models import Application
        from webapp.models import Offer
        from webapp.models.gen import gen_offer_sent

        for _ in range(1, OFFERS_SENT):
            offer = get_random_row(Offer)
            application = get_random_row(Application)
            gen_offer_sent(application=application, offer=offer)

    # -- Generate messages
    with step("Generate messages"):
        from webapp.models import Applicant
        from webapp.models.gen.Message import gen_message
        # How many of each type to generate
        from core.util import get_user_message_admin

        message_admin = get_user_message_admin()

        for _ in range(1, MESSAGES):
            applicant = get_random_row(Applicant)
            user = applicant.user
            if random.choice([True, False]):
                gen_message(user, message_admin)
            else:
                gen_message(message_admin, user)

    # -- Generate ubsuser account
    with step("Renaming one user to ubsuser"):
        applicant = get_random_row(Applicant)
        applicant.user.username = "ubsuser"
        applicant.user.email = "ubsuser@system.com"
        applicant.user.set_password('ubsuser')
        applicant.user.save()


def recalculate_constraint_rules():
    """Recalculate constraints and point rules"""
    with step("Recalculate constraints"):
        from webapp.tasks.recalculate_constraints import recalculate_constraints

        recalculate_constraints()


def recalculate_rules(include_inactive=False):
    """Recalculate constraints and point rules"""
    with step("Recalculate points"):
        from webapp.tasks.recalculate_points import recalculate_points

        recalculate_points(None, include_inactive=include_inactive)


if __name__ == "__main__":
    # Ignore all warnings, we want our output clear
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
