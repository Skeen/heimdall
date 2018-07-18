"""Unit-test for api.views."""

# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from rest_framework.test import APITestCase
from django.urls import reverse
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin
from webapp.models.gen.Tenancy import gen_tenancy


class TenancyTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the Tenancy api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.user = self.create_applicant_user()
        self.admin_user = self.create_admin_user()
        self.list_url = reverse('tenancy-list')

    def user_login(self):
        """Login the applicant user."""
        logged_in = self.client.login(username=self.userlogin['username'],
                                      password=self.userlogin['password'])
        self.assertTrue(logged_in)

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def test_reject_not_logged_in(self):
        """Attempting to get without being logged in fails."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_allow_get(self, is_admin_user):
        """Test wether users can GET content.

            Both admins and ordinary users can do this.
        """
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        [False, 403],
        [True, 200],
    ])
    #    @unittest.skip('Awaiting queryset fix')
    def test_allow_admin_write(self, is_admin_user, status):
        """Test whether user can POST.

        Admins can do this.
        Ordinary users cannot do this.
        """
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        tenancy = gen_tenancy()

        url = reverse('tenancy-detail', args=[tenancy.pk])
        response = self.client.patch(url, {"tenancy_no_suffix": 42})
        self.assertEqual(response.status_code, status)
