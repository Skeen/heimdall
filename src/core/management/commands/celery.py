# pylint: disable=W9903
"""Commands from controlling celery worker."""

from core.management.ProcessService import ProcessService
from core.management.ServiceCommand import ServiceCommand


class Command(ProcessService, ServiceCommand):
    """Commands for controlling the Celery worker.

    Examples:

        Starting the worker:

        .. code:: console

            $ python manage.py celery start

            Celery started!

        Stopping the worker:

        .. code:: console

            $ python manage.py celery stop

            Celery stopped!

        Getting worker status:

        .. code:: console

            $ python manage.py celery status

            Celery is (not) running

        Getting database log:

        .. code:: console

            $ python manage.py celery log

            Connected to amqp://guest:**@127.0.0.1:5672//
            mingle: searching for neighbors
            mingle: all alone

            ...
    """

    service_name = "Celery"
    help = 'Control the celery worker'

    command = 'celery'
    arguments = ['-A', 'heimdall', 'worker', '-l', 'info']
