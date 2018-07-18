"""Unit-test for api.views.util"""

# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from mock import MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase
from nose_parameterized import parameterized

from api.permissions import AllReadAdminWritePermission
from webapp.tests.viewtests.util import CreateUserMixin
from adminapp.tests.viewtests.util import CreateAdminMixin


class AllReadAdminWritePermissionTest(CreateAdminMixin, CreateUserMixin,
                                      APITestCase):
    """Unit-test for the AllReadAdminWritePermission"""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.permission = AllReadAdminWritePermission()
        self.factory = RequestFactory()
        self.view = MagicMock()
        self.users = {
            'admin': self.create_admin_user(),
            'authenticated': self.create_applicant_user(),
            'anonymous': AnonymousUser(),
        }

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
        ['admin'],
        ['authenticated'],
        ['anonymous'],
    ])
    def test_get_permissions(self, user):
        """Testing get permissions"""
        request = self.factory.get('/test/')
        request.user = self.users[user]
        self.assertTrue(self.permission.has_permission(request, self.view))

    @parameterized.expand([
        ['admin', True],
        ['authenticated', False],
        ['anonymous', False],
    ])
    def test_post_permissions(self, user, allowed):
        """Testing post permissions"""
        request = self.factory.post('/test/')
        request.user = self.users[user]
        self.assertEqual(self.permission.has_permission(
            request, self.view), allowed)
