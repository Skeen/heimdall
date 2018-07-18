"""This is a django-split-settings main file.

For more information read this:
* https://github.com/sobolevn/django-split-settings
"""

from split_settings.tools import optional, include

settings = [
    # Flag files
    optional('flags/debug.py'),
    optional('flags/dev.py'),
    'flags/secret_key.py',

    # Various common settings
    'common/base_dir.py',
    'common/common_settings.py',
    'common/debug_toolbar.py',
    
    # Various optional components
    optional('components/database.py'),
    optional('components/email.py'),
    optional('components/searching.py'),
    optional('components/celery.py'),

    # Load everything from here
    'auto/*.py'
]

# Include settings:
include(*settings)
