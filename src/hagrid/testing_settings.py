# pylint: disable=W9903
# pylint: disable=undefined-variable
# pylint: disable=unused-wildcard-import
"""
Django settings for testing the hagrid project.

These settings import all common settings, and then override a few if required.
This allows us to adjust behavior specificially to ensure a consistent testing
environment.
"""
# pylint: disable=wildcard-import
from hagrid.settings import *

TESTING = True
DEBUG = True
