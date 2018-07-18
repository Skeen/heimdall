"""Service like interface for django commands."""
# pylint: disable=W9903
from django.core.management.base import BaseCommand


class ServiceCommand(BaseCommand):
    """Service like interface for django commands."""

    # We expect these functions to be present
    def read_identifier(self):
        """Get an identifier to use for status, stop, log and is_running."""
        raise NotImplementedError

    def status(self, identifier):
        """Print the running/stopped/error status of the service."""
        raise NotImplementedError

    def stop(self, identifier):
        """Stop the service."""
        raise NotImplementedError

    def is_running(self, identifier):
        """Check if the service is running.

        Returns:
            bool: True if running, false otherwise.
        """
        raise NotImplementedError

    def start(self):
        """Start the service.

        Returns:
            any: Specific to the service type.
        """
        raise NotImplementedError

    def log(self, identifier):
        """Print the log of the service."""
        raise NotImplementedError

    # And this variable
    service_name = None
    custom_commands = None

    def add_arguments(self, parser):
        """Setup arguments to accept for this command."""
        choices = ['start', 'stop', 'status', 'log']
        if self.custom_commands is not None:
            choices.extend(self.custom_commands)
        parser.add_argument('command',
                            help='The command to run',
                            choices=choices)
        parser.add_argument('--force',
                            help='ignore existent containers',
                            action='store_true')

    def handle(self, *args, **options):
        """Handle the incoming request, delegating to submethods."""
        # Read identifier for subfunctions
        # TODO: Interface
        identifier = self.read_identifier()

        if options['command'] == 'status':
            self.status(identifier)
        elif options['command'] == 'stop':
            self.stop(identifier)
        elif options['command'] == 'start':
            if self.is_running(identifier) and options['force'] is False:
                print self.service_name + " already running. Aborting."
            else:
                self.start()
        elif options['command'] == 'log':
            self.log(identifier)
        elif options['command'] in self.custom_commands:
            custom_command = getattr(self, options['command'])
            custom_command(identifier)
        else:
            raise ValueError('Unexpected command')
