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

from webapp.models import ApplicantCommitteeProperties


# pylint: disable=line-too-long
class ApplicantCommitteePropertiesTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for com_prop-list and attach_offer_com_prop-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_applicant_user()
        self.com_prop = self.user.applicant.committee_properties.first()

        self.list_url = reverse('applicantcommitteeproperties-list')
        self.detail_url = reverse(
            'applicantcommitteeproperties-detail', args=[self.com_prop.pk]
        )

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
        [False, True],
        [True, False],
    ])
    def test_list_accept_logged_in(self, is_admin_user, rejected):
        """Test that the com_prop list shows up as expected."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        from webapp.models.gen import gen_applicant
        gen_applicant()

        response = self.client.get(self.list_url)
        if rejected:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(ApplicantCommitteeProperties.objects.count(), 2)
            self.assertEqual(response.data['count'], 1)
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['next'], None)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(ApplicantCommitteeProperties.objects.count(), 2)
            self.assertEqual(response.data['count'], 2)
            self.assertEqual(len(response.data['results']), 2)
            self.assertEqual(response.data['next'], None)

    @parameterized.expand([
        [False, True],
        [True, False],
    ])
    def test_detail_accept_logged_in(self, is_admin_user, rejected):
        """Test that the user list shows up as expected."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.detail_url)
        if rejected:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['pk'], self.com_prop.pk)
            self.assertNotIn('num_rejections', response.data)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['pk'], self.com_prop.pk)
            self.assertEqual(response.data['num_rejections'],
                             self.com_prop.num_rejections)
