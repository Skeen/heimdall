
"""Unit-test for api.views."""

# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from rest_framework.test import APITestCase
from django.urls import reverse
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin
from webapp.models import ApprobationCommittee
from webapp.models import PointValue
from webapp.models.gen.Application import gen_application
from webapp.models.gen.Applicant import gen_applicant
from webapp.models.util import APPLICANT_STATUS_ACTIVE
from webapp.tasks.recalculate_constraints import recalculate_constraints


class PointValueTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the PointValue api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.user = self.create_applicant_user()
        self.admin_user = self.create_admin_user()
        self.list_url = reverse('pointvalue-list')
        self.applicant = gen_applicant()
        self.ciu = ApprobationCommittee.objects.get(abbreviation='CIU')
        gen_application(appl_target=self.ciu, applicants=[self.applicant])
        self.com_prop = self.applicant.get_committee_properties(self.ciu, True)
        self.com_prop.active_status = APPLICANT_STATUS_ACTIVE
        self.com_prop.save()
        recalculate_constraints()

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
        """Tests that admin and non-admin users can get list."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_filter_applicant(self, is_admin_user):
        """Test applicant filter."""
        expected_count = 0
        # Login
        if is_admin_user:
            expected_count = PointValue.objects.count()
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url,
                                   {'applicant1': self.applicant.pk})

        self.assertEqual(response.data['count'], expected_count)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_filter_application_target(self, use_ciu):
        """Test application target filter."""
        self.admin_login()
        expected_count = None
        target = None
        if use_ciu:
            expected_count = PointValue.objects.count()
            target = self.ciu.pk
        else:
            expected_count = 0
            target = ApprobationCommittee.objects.get(abbreviation='RIU').pk
        response = self.client.get(self.list_url,
                                   {'appl_target': target})

        self.assertEqual(response.data['count'], expected_count)

    @parameterized.expand([
        [1, 0],
        [2, 1],
        [3, -1],
        [None, 0],
    ])
    def test_filter_adjusted(self, filter_value, count_adjustment):
        """Tests adjusted filter."""
        expected_count = PointValue.objects.count()
        if count_adjustment:
            expected_count = (expected_count+count_adjustment) % expected_count
        adjust_value = PointValue.objects.first()
        adjust_value.manual_adjust = 42
        adjust_value.save()
        self.admin_login()
        response = self.client.get(self.list_url,
                                   {'adjusted': filter_value})
        self.assertEqual(response.data['count'], expected_count)

    @parameterized.expand([
        [1, 0],
        [2, 1],
        [3, -1],
        [None, 0],
    ])
    def test_filter_override(self, filter_value, count_adjustment):
        """Tests override filter."""
        expected_count = PointValue.objects.count()
        if count_adjustment:
            expected_count = (expected_count+count_adjustment) % expected_count
        override_value = PointValue.objects.first()
        override_value.manual_override = True
        override_value.save()
        self.admin_login()
        response = self.client.get(self.list_url,
                                   {'override': filter_value})
        self.assertEqual(response.data['count'], expected_count)
