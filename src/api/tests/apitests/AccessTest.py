"""Unit-tests for api.views

Todo:
    Refactor logged-in required redirects as mixin.
"""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from rest_framework.test import APITestCase
from django.urls import reverse
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin

from webapp.models.gen.Address import gen_address


class AccessTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Verify only admin is permitted access."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_applicant_user()
        # urls
        address = gen_address()
        self.list_url = reverse('address-list')
        self.detail_url = reverse('address-detail', args=[address.pk])

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

    @parameterized.expand([
        [lambda self: self.list_url],
        [lambda self: self.detail_url],
    ])
    def test_X_reject_not_logged_in(self, url_function):
        """Not logged in yields no access."""
        response = self.client.get(url_function(self))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_list_accept_logged_in(self, is_admin_user):
        """Only admin can see resulsts."""
        # TODO: Assert that other users are only shown to admins
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200 if is_admin_user else 403)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_detail_accept_logged_in(self, is_admin_user):
        """Test that the user list shows up as expected."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200 if is_admin_user else 403)
