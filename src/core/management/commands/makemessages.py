# pylint: disable=W9903
"""Command from makemessages."""

from django.core.management.commands import makemessages


class Command(makemessages.Command):
    """Extend makemessages, to look for additional aliases.

    Adds the _lazy alias to the lookup scheme.
    """

    xgettext_options = (makemessages.Command.xgettext_options +
                        ['--keyword=_lazy'])
