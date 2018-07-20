"""Docker service mixin class."""
# pylint: disable=W9903
# TODO: Abstract baseclass Service with ProcessService
import sys
import docker

from requests.adapters import ConnectionError


class DockerService(object):
    """Docker service mixin class."""

    service_name = None
    image = None
    ports = None
    volumes = None
    environment = None

    def __init__(self):
        super(DockerService, self).__init__()
        # Setup docker client
        self.client = docker.from_env(version='auto')
        # Setup dockerid path
        # pylint: disable=no-name-in-module
        from hagrid.settings import BASE_DIR
        self.dockerid_path = (BASE_DIR + '/database/' +
                              self.service_name + '_dockerid')

    def _write_dockerid(self, container):
        """Write the containers id to a file."""
        with open(self.dockerid_path, "w") as text_file:
            text_file.write(container.id)

    def _read_dockerid(self):
        """Read the containers id from a file."""
        data = None
        try:
            with open(self.dockerid_path, "r") as text_file:
                data = text_file.read()
        except IOError:
            pass
        return data

    def log(self, identifier):
        """Print the log of the docker instance."""
        try:
            container = self.client.containers.get(identifier)
            print container.logs()
        except docker.errors.NotFound:
            print "Docker not found, check manually"
            sys.exit(1)
        except docker.errors.NullResource:
            print "Resource ID not given, check manually"
            sys.exit(1)

    def setup_settings(self, container, portmap):
        """Write any settings files required."""
        pass

    def start(self):
        """Start the docker instance."""
        # Check validity of image name
        # pylint: disable=unsupported-membership-test
        if ":" not in self.image:
            print "No image version specified."
            sys.exit(1)

        # Start docker
        try:
            container = self.client.containers.run(
                image=self.image,
                detach=True,
                ports=self.ports,
                volumes=self.volumes,
                restart_policy={
                    "Name": "always",
                },
                environment=self.environment,
            )
            self._write_dockerid(container)
            print self.service_name + " started!"
            container.reload()
            portmap = container.attrs['NetworkSettings']['Ports']
            self.setup_settings(container, portmap)
            return container
        except ConnectionError:
            print ""
            print "Unable to connect to docker daemon."
            print "Please verify that the docker daemon is running:"
            print ""
            print "$ docker run hello-world"
            print ""
            print "Expected output: 'Hello from Docker!'"
            print ""
            print "If this output does not occur, please reinstall docker:"
            print "* https://docs.docker.com/engine/installation/"
            print ""
            sys.exit(1)

    def get_container(self, identifier):
        """Get the docker container instance from the identifier."""
        try:
            container = self.client.containers.get(identifier)
            return container
        except docker.errors.NotFound:
            print "Docker not found, check manually"
            sys.exit(1)
        except docker.errors.NullResource:
            print "Resource ID not given, check manually"
            sys.exit(1)

    def stop(self, identifier):
        """Stop the docker instance."""
        container = self.get_container(identifier)
        container.stop()
        container.remove()
        print self.service_name + " stopped!"

    def is_running(self, identifier):
        """Get the status of the docker instance."""
        try:
            container = self.client.containers.get(identifier)
            return container.status == 'running'
        except docker.errors.NotFound:
            return False
        except docker.errors.NullResource:
            return False

    def status(self, identifier):
        """Print the status of the docker instance."""
        status = self.is_running(identifier)
        if status:
            print self.service_name + " is running"
        else:
            print self.service_name + " is NOT running"

    def read_identifier(self):
        """Return docker id as our identifier."""
        return self._read_dockerid()
