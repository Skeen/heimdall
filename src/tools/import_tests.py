#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W9903
"""Run this to see test import errors."""
import os
import sys
import django


def main():
    """Run this to see test import errors."""
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "heimdall.settings")
    django.setup()

    # pylint: disable=unused-variable
    import webapp.tests
    import adminapp.tests
    import core.tests
    import api.tests
    import data_migration.tests
    # import healthcheck.tests


if __name__ == "__main__":
    main()
