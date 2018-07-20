#!/usr/bin/env python
# pylint: disable=W9903
"""Tool for managing django applications."""
import os
import sys


def main():
    """Run django project commands.

    Invoke by running:

    .. code:: bash

        python manage.py {{TASK}}

    For details see the django-admin: :django:django-admin:`help`
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hagrid.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            # flake8: noqa # pylint: disable=unused-variable
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    #if 'test' in sys.argv:
    #    print "For testing, please run 'python runtests.py' instead."
    #    exit(1)

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
