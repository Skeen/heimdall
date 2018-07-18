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

from webapp.models.gen.Offer import gen_offer
from webapp.models import OfferSent


class GenerateOfferSentTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Test gen_offer_sent-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_applicant_user()

        self.offer = gen_offer()
        # urls
        self.url = reverse('gen_offer_sent-list')

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
        [False],
        [True],
    ])
    def test_reject_get(self, is_admin_user):
        """Get is disallowed."""
        # TODO: Assert that other users are only shown to admins
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405 if is_admin_user else 403)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_accept_logged_in(self, is_admin_user):
        """Only admin can post results."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400 if is_admin_user else 403)

    @parameterized.expand([
        [lambda user: 'alfa',
         lambda offer: 42,
         400],
        [lambda user: 'alfa',
         lambda offer: offer.pk,
         400],
        [lambda user: user.applicant.applicant_number,
         lambda offer: 42,
         400],
        [lambda user: user.applicant.applicant_number,
         lambda offer: offer.pk,
         201],
    ])
    def test_generate_offer_sent(self, fun_applica_no,
                                 fun_offer_pk, expected_result):
        """Test that the user list shows up as expected."""
        self.admin_login()

        applicant_no = fun_applica_no(self.user)
        offer_pk = fun_offer_pk(self.offer)
        self.assertEqual(OfferSent.objects.count(), 0)
        response = self.client.post(self.url, {
            'applicant_no': applicant_no,
            'offer_pk': offer_pk,
        })
        self.assertEqual(response.status_code, expected_result)
        self.assertEqual(OfferSent.objects.count(),
                         1 if expected_result is 201 else 0)
