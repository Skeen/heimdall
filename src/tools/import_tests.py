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
    import core.tests
    import api.tests


if __name__ == "__main__":
    main()
