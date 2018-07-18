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


class UserTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the User api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_applicant_user()
        # urls
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', args=[self.user.pk])

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
        """Test that the user list shows up as expected."""
        # TODO: Assert that other users are only shown to admins
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        # Test we get 2 users back
        from django.contrib.auth import get_user_model
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)
        # Test users
        for i, user in {0: self.admin_user, 1: self.user}.iteritems():
            self.assertEqual(
                response.data['results'][i]['first_name'],
                user.first_name
            )
            self.assertEqual(
                response.data['results'][i]['last_name'],
                user.last_name
            )
            self.assertEqual(
                response.data['results'][i]['applicant_pk'],
                (user.applicant.pk if hasattr(user, 'applicant') else None)
            )
            self.assertEqual(
                response.data['results'][i]['is_staff'],
                user.is_staff
            )
            self.assertEqual(
                'username' in response.data['results'][i],
                is_admin_user
            )

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
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['is_staff'], self.user.is_staff)
        self.assertEqual('username' in response.data, is_admin_user)
