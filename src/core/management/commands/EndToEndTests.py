# pylint: disable=W9903
"""Run all end-to-end tests, and report the status."""
import subprocess
import sys

from django.core.management.base import BaseCommand

from django.conf import settings
from django.test.utils import get_runner
from django.test import LiveServerTestCase
from django.core import serializers


class TestCafeTests(LiveServerTestCase):
    """Run tests with test-cafe."""

    @classmethod
    def setUpClass(cls):
        """Load test fixture with try-catch statement."""
        super(TestCafeTests, cls).setUpClass()
        # Load test fixture
        fixture_file = 'core/fixtures/test_database.json'
        fixture = open(fixture_file)
        objects = serializers.deserialize(
            'json',
            fixture,
            ignorenonexistent=True
        )
        for obj in objects:
            try:
                obj.save()
            except Exception as exc:  # pylint: disable=broad-except
                print "Couldn't save: " + str(obj) + "(" + str(exc) + ")"
        fixture.close()

    # pylint: disable=no-self-use
    def install_npm_dependencies(self, test_dir):
        """Install the npm dependencies for the frontend."""
        process = subprocess.Popen(["npm", "install"], cwd=test_dir)
        exit_status = process.wait()
        return exit_status

    # pylint: disable=no-self-use
    def build_frontend(self, test_dir):
        """Build the VueJS frontend."""
        process = subprocess.Popen(["npm", "run", "build"], cwd=test_dir)
        exit_status = process.wait()
        return exit_status

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    def test_with_testcafe(self):
        """Test the adminapp frontend with test-cafe."""
        # TODO: Somehow report x/y tests to python, maybe a testdiscoverer?
        from core.util import get_user_ubs_admin
        get_user_ubs_admin()

        # This is the folder which contains the package.json file
        # pylint: disable=no-name-in-module
        from heimdall.settings import BASE_DIR
        adminapp_test_dir = BASE_DIR + r'/adminapp/frontend/'
        webapp_test_dir = BASE_DIR + r'/webapp/frontend/'

        # Ensure that we loaded the fixture
        from webapp.models import Applicant
        self.assertEqual(Applicant.objects.count(), 49)

        # Install npm dependencies and build frontend
        print "---------------------------"
        print "Installing npm dependencies"
        print "---------------------------"
        adminapp_install_status = self.install_npm_dependencies(
            adminapp_test_dir
        )
        webapp_install_status = self.install_npm_dependencies(
            webapp_test_dir
        )
        print ""
        print "Install status (adminapp): " + str(adminapp_install_status)
        print "Install status (webapp): " + str(webapp_install_status)
        print ""

        print "-----------------"
        print "Running npm build"
        print "-----------------"
        adminapp_build_status = self.build_frontend(adminapp_test_dir)
        webapp_build_status = self.build_frontend(webapp_test_dir)
        print ""
        print "Build status (adminapp): " + str(adminapp_build_status)
        print "Build status (webapp): " + str(webapp_build_status)
        print ""

        # Collect statics
        from django.core.management import call_command
        print "---------------------"
        print "Running collectstatic"
        print "---------------------"
        call_command('collectstatic', '--noinput')
        print ""
        print ""

        from urlparse import urlparse
        parsed = urlparse(self.live_server_url)

        # Start the testing process
        print "----------------------"
        print "Running testcafe tests"
        print "----------------------"
        print "Against url: " + str(parsed.hostname) + ':' + str(parsed.port)
        print "----------------------"
        process = subprocess.Popen([
            "node_modules/testcafe/bin/testcafe-with-v8-flag-filter.js",
            "'chromium:headless --no-sandbox --lang=da-dk'",
            "tests/*.js",
            # "../../webapp/frontend/tests/*.js",
            "-r",
            "xunit:res.xml",
            "--testurl",
            str(parsed.hostname) + ':' + str(parsed.port)
        ], cwd=adminapp_test_dir)
        # Exit status is the number of failed test-cases
        exit_status = process.wait()
        import xml.etree.ElementTree
        res = xml.etree.ElementTree.parse(
            adminapp_test_dir + 'res.xml'
        ).getroot()
        print ""
        print "Status:"
        print res.attrib['tests'] + " tests in " + res.attrib['time'] + "s"
        print res.attrib['skipped'] + " tests were skipped"
        print res.attrib['failures'] + " tests failed"
        print res.attrib['errors'] + " tests had errors"
        print ""

        # Assert that no tests failed
        self.assertEqual(exit_status, 0,
                         msg="Expected the number of failed tests to be zero")


class Command(BaseCommand):
    """Run all end-to-end tests, and report the status.

    Examples:

        Invoke by running:

        .. code:: bash

            ./runlivetests.sh

    Note:

        This requires the :code:`adminapp/frontend` and :code:`webapp/frontend`
        projects to have been build prior, and that a chrome/chromium headless
        browser is available on :code:`PATH`.
    """

    help = 'Run all end-to-end tests, and report the status.'

    def handle(self, *args, **options):
        # Setup test-runner and run tests
        test_runner = get_runner(settings)(interactive=False)
        # Run tests
        failures = test_runner.run_tests(
            ['core.management.commands.EndToEndTests']
        )
        # Report back
        sys.exit(bool(failures))
