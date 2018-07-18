"""Unit-tests for api.views

Todo:
    Refactor logged-in required redirects as mixin.
"""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from freezegun import freeze_time
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_text
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin

from webapp.models import Application
from webapp.models.gen import gen_applicant
from webapp.models.gen import gen_application
from webapp.models.gen import gen_tenancy
from webapp.models import Dictionary
from webapp.models import PointRule
from webapp.models import util


# pylint: disable=too-many-instance-attributes
class ApplicationTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the Application api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_user()
        gen_applicant(user=self.user)

        self.tenancy = gen_tenancy()

        from webapp.models.gen import gen_education
        from webapp.models.util import EDU_STATUS_IN_PROGRESS
        from dateutil.relativedelta import relativedelta
        from webapp.models.util import APPLICANT_STATUS_ACTIVE

        self.application1 = gen_application(
            appl_target=self.tenancy,
        )
        self.applicant1 = self.application1.applicants.first()

        self.applicant1.educations.all().delete()
        self.applicant1.save()
        gen_education(self.applicant1, status=EDU_STATUS_IN_PROGRESS)
        self.applicant1.save()

        appl1_props = self.applicant1.committee_properties.first()
        appl1_props.active_status = APPLICANT_STATUS_ACTIVE
        appl1_props.save()

        # Setup status periods using freezegun
        with freeze_time(timezone.now() - relativedelta(days=7)):
            self.application2 = gen_application(
                appl_target=self.tenancy,
            )
            self.applicant2 = self.application2.applicants.first()

            self.applicant2.educations.all().delete()
            self.applicant2.save()
            gen_education(self.applicant2, status=EDU_STATUS_IN_PROGRESS)
            self.applicant2.save()

            appl2_props = self.applicant2.committee_properties.first()
            appl2_props.active_status = APPLICANT_STATUS_ACTIVE
            appl2_props.save()

        # Setup the date ranking rule
        committee = self.tenancy.get_committee()
        config_dict = Dictionary.objects.create()
        config_dict['points_per_day_active'] = smart_text(1)
        config_dict['points_per_day_abroad'] = smart_text(0)
        config_dict['points_abroad_max'] = smart_text(0)
        self.rule = PointRule.objects.create(
            name='Anciennitet',
            rule_text="",
            # pylint: disable=line-too-long
            impl_class='webapp.domain.pointrules.DateRankingRule',
            defined_on_target=committee,
            values_on_level=util.HIERARCHY_COMMITTEE,
            config_dict=config_dict,
            periodic=True
        )

        # Recalculate all points
        from webapp.tasks.recalculate_points import recalculate_points
        recalculate_points()

        self.url = reverse('application-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def user_login(self):
        """Login the applicant user."""
        logged_in = self.client.login(username=self.userlogin['username'],
                                      password=self.userlogin['password'])
        self.assertTrue(logged_in)

    def test_list_all(self):
        """Test all listed."""
        self.admin_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 3)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['next'], None)

    def test_two_applicants(self):
        """Test all listed."""
        self.admin_login()

        from webapp.models.util import APPLICANT_STATUS_HOLD

        applicant31 = gen_applicant(active_status=APPLICANT_STATUS_HOLD)
        applicant32 = gen_applicant()
        self.application1 = gen_application(
            appl_target=self.tenancy,
            applicants=[applicant31, applicant32]
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 5)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['next'], None)

    def test_list_user(self):
        """Test list for user."""
        applications = self.user.applicant.applications.all()
        self.user_login()

        response = self.client.get(self.url)
        results = response.data['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 3)
        self.assertEqual(response.data['count'], applications.count())
        self.assertEqual(len(results), applications.count())
        self.assertEqual(response.data['next'], None)
        self.assertEqual(results[0]['pk'], applications[0].pk)

    def test_list_waiting_list(self):
        """Test tenancy waiting list."""
        self.admin_login()

        response = self.client.get(self.url, {'waiting_list': self.tenancy.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 3)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)
        for result in response.data['results']:
            self.assertEqual(
                result["max_points"],
                "Warning: Points only presented when used for ordering"
            )

    @parameterized.expand([
        ['points', 0, 7],
        ['-points', 7, 0],
    ])
    def test_list_waiting_list_points(self, order_by, points1, points2):
        """Test points for waiting list."""
        self.admin_login()

        response = self.client.get(self.url, {
            'waiting_list': self.tenancy.pk,
            'order_by': order_by + "$" + str(self.tenancy.pk),
        })
        results = response.data['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 3)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(results), 2)
        self.assertEqual(response.data['next'], None)

        self.assertEqual(results[0]["max_points"], points1)
        self.assertEqual(results[1]["max_points"], points2)

    def test_position_on_waitinglist_alone(self):
        """Test that we show up first on waitinglist."""
        applicant = self.user.applicant
        application = applicant.applications.first()
        tenancy = application.appl_target.tenancy
        building = tenancy.get_building
        self.url = (reverse('get_position-detail', args=[building.pk]) +
                    "?tenancies=" + str(tenancy.pk))
        self.user_login()

        # Fire and get a reply
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 1)

#    def test_position_on_waitinglist_second(self):
#        """Test that we show up second on waitinglist."""
#        applicant = self.user.applicant
#        application = applicant.applications.first()
#        tenancy = application.appl_target.tenancy
#        building = tenancy.get_building
#
#        applicant2 = gen_applicant(tenancy=tenancy)
#        from webapp.models import PointValue
#        PointValue.objects.create(
#            rule=self.rule,
#            appl_target=tenancy,
#            applicant1=applicant2,
#            reason=None,
#            computed_value=1000,
#        )
#
#        self.url = (reverse('get_position-detail', args=[building.pk]) +
#                    "?tenancies=" + str(tenancy.pk))
#        self.user_login()
#
#        # Fire and get a reply
#        response = self.client.get(self.url)
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, 2)
