#!/usr/bin/env python
# TODO: Unify with E2ETests
# pylint: disable=W9903
"""Tool for running unit-tests."""
import os
import sys

import django
from django.test.utils import get_runner
from coverage import Coverage


def num_cores():
    """Find the number of cores on the system.

    Returns:
        int: Number of cores on the system.
    """
    import multiprocessing
    return multiprocessing.cpu_count()


def main(tests):
    """Run all unit-tests, and report the status.

    Invoke by running:

    .. code:: bash

        ./runtests.sh

    After running tests, coverage can be reported by invoking:

    .. code:: bash

        coverage report
    """
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "heimdall.testing_settings"
    )

    # For configuration details, see:
    # - http://coverage.readthedocs.io/en/latest/api_coverage.html
    cov = Coverage(config_file=True)
    cov.start()

    # Setup django
    django.setup()

    from django.conf import settings
    if settings.TESTING is False:
        print "WARNING: Running tests without TESTING=TRUE"

    if settings.DEBUG is False:
        print "WARNING: Running tests without DEBUG=TRUE"

    # Setup test-runner and run tests
    test_runner = get_runner(settings)(parallel=num_cores(), interactive=False)
    failures = test_runner.run_tests(tests)

    # Save coverage
    cov.save()

    # Report back
    sys.exit(bool(failures))


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    import warnings
    with warnings.catch_warnings():
        # Setup the warning handling stack.
        # Currently a 3 layer stack, where warning fall through the higher
        # layers, until they hit a layer for which a rule applies.

        # Lowest level, every warning dropping through is an error.
        for category in [Warning]:
            warnings.filterwarnings(action="error", category=category)

        # Middle level, deprecation are ignored globally.
        for category in [DeprecationWarning, PendingDeprecationWarning,
                         ImportWarning]:
            warnings.filterwarnings(action="ignore", category=category)

        # Top level, depcrecation warnings are thrown from our own code.
        for category in [DeprecationWarning, PendingDeprecationWarning,
                         ImportWarning]:
            warnings.filterwarnings(
                action="error",
                category=category,
                module='heimdall|core|api',
            )

        # pylint: disable=invalid-name
        argv = sys.argv
        # pylint: disable=invalid-name
        specific_test = argv[1] if len(argv) > 1 else None

        if specific_test:
            main([specific_test])
        else:
            main([
                'core.tests',
                'api.tests',
            ])
