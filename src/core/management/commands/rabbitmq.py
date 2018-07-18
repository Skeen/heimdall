# pylint: disable=W9903
"""Commands from controlling RabbitMQ."""

from core.management.DockerService import DockerService
from core.management.ServiceCommand import ServiceCommand


class Command(DockerService, ServiceCommand):
    """Commands for controlling RabbitMQ.

    Examples:

        Starting the message queue:

        .. code:: console

            $ python manage.py rabbitmq start

            Rabbitmq started!

        Stopping the message queue:

        .. code:: console

            $ python manage.py rabbitmq stop

            Rabbitmq stopped!

        Getting message queue status:

        .. code:: console

            $ python manage.py rabbitmq status

            Rabbitmq is (not) running

        Getting message queue log:

        .. code:: console

            $ python manage.py rabbitmq log

              RabbitMQ 3.6.6. Copyright (C) 2007-2016 Pivotal Software, Inc.
              Licensed under the MPL.  See http://www.rabbitmq.com/

              Starting broker...

              ...

    Note:

        A running docker daemon is required to run the above commands.

        Installing docker can be done by following the guides present at:

        * https://docs.docker.com/engine/installation/
    """

    service_name = 'RabbitMQ'
    help = 'Control the rabbitmq message queue'

    image = 'rabbitmq:3.6-management'
    ports = {
        '5672/tcp': 5672,
        '15672/tcp': 15672,
    }
