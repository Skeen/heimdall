# pylint: disable=W9903
"""Commands from controlling celery beater."""
from core.management.ProcessService import ProcessService
from core.management.ServiceCommand import ServiceCommand


class Command(ProcessService, ServiceCommand):
    """Commands for controlling the Celery beat.

    Examples:

        Starting the beat:

        .. code:: console

            $ python manage.py celery start

            Celery beat started!

        Stopping the beat:

        .. code:: console

            $ python manage.py celery stop

            Celery beat stopped!

        Getting beat status:

        .. code:: console

            $ python manage.py celery status

            Celery beat is (not) running

        Getting database log:

        .. code:: console

            $ python manage.py celery log

            beat: Starting...
            Writing entries...
            Writing entries...

            ...
    """

    service_name = "Celery_Beat"
    help = 'Control the celery beat'

    arguments = [
        'beat',
        '--app', 'heimdall',
        '--loglevel', 'info',
        '--scheduler', 'django',
    ]
    command = 'celery'
