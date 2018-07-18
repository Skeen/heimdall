# pylint: disable=W9903
"""Command to build documentation."""

from django.core.management.base import BaseCommand, CommandError
from subprocess import call

class Command(BaseCommand):
    """Command to build documentation."""

    help = 'Builds the documentation.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        sphinx_build_executable = "sphinx-build"
        sphinx_apidoc_executable = "sphinx-apidoc"

        # pylint: disable=no-name-in-module
        from heimdall.settings import BASE_DIR
        source_dir = BASE_DIR + '/docs/'
        build_dir = BASE_DIR + '/docs/_build/'
        autogen_dir = BASE_DIR + '/docs/_autogen/'

        modules = ["adminapp", "webapp", "healthcheck", "core", "api", "docs"]

        # Generate API documentation for each module
        for module in modules:
            call([sphinx_apidoc_executable, "-o", autogen_dir + module + "/",
                  BASE_DIR + "/" + module])
        
        # Generate an API index
        with open(autogen_dir + 'autoapi.rst', 'w') as autoapi:
            autoapi.write(".. toctree::\n")
            autoapi.write("\n")
            for module in modules:
                autoapi.write("    /_autogen/" + module + "/modules.rst\n")

        # Build the documentation
        call([sphinx_build_executable, "-M", "html", source_dir, build_dir])
