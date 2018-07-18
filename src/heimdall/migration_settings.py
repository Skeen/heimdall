# pylint: disable=W9903
# pylint: disable=undefined-variable
# pylint: disable=unused-wildcard-import
"""
Django settings for data migrating the heimdall project.

These settings import all common settings, and then override a few if required.
This allows us to adjust behavior specificially to ensure a good migration
environment.
"""
# pylint: disable=wildcard-import

from heimdall.settings import *

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    }
}

if 'HAYSTACK_SIGNAL_PROCESSOR' in globals():
    print "Cleaning signal processor."
    del HAYSTACK_SIGNAL_PROCESSOR
