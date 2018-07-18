"""Process service mixin class."""
# pylint: disable=W9903
import os
import signal
import subprocess

from core.util import time_limit
from core.util import TimeoutException
from core.management.util import process_alive
from core.management.util import waitpid

from django.utils.encoding import smart_text


class ProcessService(object):
    """Process service mixin class."""

    service_name = None
    command = None
    arguments = None

    def __init__(self):
        super(ProcessService, self).__init__()
        # Setup pid_path path
        # pylint: disable=no-name-in-module
        from heimdall.settings import BASE_DIR
        self.pid_path = BASE_DIR + '/database/' + self.service_name + '_pid'
        # Setup log path
        self.log_path = BASE_DIR + '/database/' + self.service_name + '_log'

    def _write_pid(self, process):
        """Write the process pid to a file."""
        with open(self.pid_path, "w") as text_file:
            text_file.write(smart_text(process.pid))

    def _read_pid(self):
        """Read the process pid from a file."""
        data = None
        try:
            with open(self.pid_path, "r") as text_file:
                data = text_file.read()
        except IOError:
            pass
        return data

    # pylint: disable=unused-argument
    def log(self, pid):
        """Print the log of the process."""
        with open(self.log_path, "r") as text_file:
            print text_file.read()

    def start(self):
        """Start the process."""
        # Open the log file
        log_file = open(self.log_path, "w")
        # Prepare the command
        command = [self.command]
        command.extend(self.arguments)
        # Start the process
        process = subprocess.Popen(
            command,
            stdout=log_file,
            stderr=subprocess.STDOUT)
        self._write_pid(process)
        print self.service_name + " started!"
        return process

    def stop(self, pid):
        """Stop the process."""
        if self.is_running(pid) is False:
            print "PID not found, check manually"
            return

        try:
            with time_limit(10):
                os.kill(pid, signal.SIGTERM)
                waitpid(pid)
        except TimeoutException:
            with time_limit(10):
                os.kill(pid, signal.SIGKILL)
                waitpid(pid)

    def is_running(self, pid):
            # pylint: disable=no-self-use
        """Check if the process is running."""
        return process_alive(pid)

    def status(self, pid):
        """Print the status of the process."""
        status = self.is_running(pid)
        if status:
            print self.service_name + " is running"
        else:
            print self.service_name + " is NOT running"

    def read_identifier(self):
        """Return PID as our identifier."""
        pid = None
        try:
            pid = int(self._read_pid())
        except TypeError:
            pass
        return pid
