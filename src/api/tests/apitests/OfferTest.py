"""Unit-tests for api.views

Todo:
    Refactor logged-in required redirects as mixin.
"""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
import datetime

import pytz
from rest_framework.test import APITestCase
from django.urls import reverse
from nose_parameterized import parameterized

from api.views.Offer import OfferViewSet
from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin

from webapp.models import Offer
from webapp.models.gen.Offer import gen_offer
from webapp.models.gen.OfferSent import gen_offer_sent
from webapp.models.gen.Tenancy import gen_tenancy
from webapp.models.gen.Application import gen_application


class CreateOfferTest(CreateAdminMixin, APITestCase):
    """Unit-tests for send_offer-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.tenancy = gen_tenancy()
        self.url = reverse('offer-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def test_create_offer(self):
        """Test that we can create offer.

        Verify that tenancy.available_date is transferred to offer.
        """
        avail_date = datetime.date(year=2000, month=1, day=1)
        self.tenancy.available_date = avail_date

        # Set publishtime and no delete time to ensure tenancy is available
        tzinfo = pytz.timezone('UTC')
        self.tenancy.publishtime = tzinfo.localize(
            datetime.datetime(year=2000, month=1, day=1)
        )
        self.tenancy.deletetime = None
        self.tenancy.save()
        self.admin_login()

        response = self.client.post(self.url, {
            'tenancy_pk': self.tenancy.pk,
            'assigned_to_pks': [],
            'created_by_pk': self.admin_user.pk
        })

        self.assertEqual(response.status_code, 201)
        offer = Offer.objects.all().first()
        self.assertEqual(offer.tenancy_avail_date,
                         avail_date)


class SendOfferTest(CreateAdminMixin, APITestCase):
    """Unit-tests for send_offer-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        self.admin_user = self.create_admin_user()

        self.tenancy = gen_tenancy()

        self.offer = gen_offer(
            status=Offer.STATUS_EDITING,
            tenancy=self.tenancy
        )
        self.offer.offer_message = "placeholder"
        self.offer.save()

        from webapp.models.gen import gen_education
        from webapp.models.util import EDU_STATUS_IN_PROGRESS
        from webapp.models.util import APPLICANT_STATUS_ACTIVE

        self.application = gen_application(
            appl_target=self.tenancy,
        )
        self.applicant = self.application.applicants.first()

        self.applicant.educations.all().delete()
        self.applicant.save()
        gen_education(self.applicant, status=EDU_STATUS_IN_PROGRESS)
        self.applicant.save()

        appl_props = self.applicant.committee_properties.first()
        appl_props.active_status = APPLICANT_STATUS_ACTIVE
        appl_props.save()

        gen_offer_sent(
            offer=self.offer,
            application=self.application
        )

        self.url = reverse('send_offer-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def test_send_offer(self):
        """Test that we can send offer."""
        self.admin_login()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.offer.status, Offer.STATUS_OPEN)
        self.assertEqual(response.data, {})

    def test_no_message(self):
        """Test message is required to send."""
        self.admin_login()

        self.offer.offer_message = None
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_EDITING)
        self.assertEqual(response.data['offer_pk'], ['No offer message set!'])

    def test_wrong_status(self):
        """Test status editing is required to send."""
        self.admin_login()

        self.offer.status = Offer.STATUS_ABORTED
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_ABORTED)
        self.assertEqual(
            response.data['offer_pk'],
            ['Can only send offers, with status editing.']
        )

    def test_no_deadline(self):
        """Test deadline is required to send."""
        self.admin_login()

        self.offer.deadline = None
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_EDITING)
        self.assertEqual(response.data['offer_pk'], ['No deadline set!'])

    def test_no_reciever(self):
        """Test at least one receiver is required."""
        self.admin_login()

        self.offer.offers_sent.all().delete()
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_EDITING)
        self.assertEqual(response.data['offer_pk'], ['No offer recievers!'])

    def test_no_valid(self):
        """Test receiving application is required to have active applicant."""
        self.admin_login()

        self.applicant.trigger_default_quarantine(self.tenancy)
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_EDITING)
        self.assertEqual(
            "No applicants can recieve an offer",
            response.data['offer_pk'][0]
        )


class CloseOfferTest(CreateAdminMixin, APITestCase):
    """Unit-tests for close_offer-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        self.admin_user = self.create_admin_user()

        self.tenancy = gen_tenancy()

        self.offer = gen_offer(
            status=Offer.STATUS_FINISHED,
            tenancy=self.tenancy
        )
        self.offer.save()

        from webapp.models.gen import gen_education
        from webapp.models.util import EDU_STATUS_IN_PROGRESS
        from webapp.models.util import APPLICANT_STATUS_ACTIVE

        self.application = gen_application(
            appl_target=self.tenancy,
        )
        self.applicant = self.application.applicants.first()

        self.applicant.educations.all().delete()
        self.applicant.save()
        gen_education(self.applicant, status=EDU_STATUS_IN_PROGRESS)
        self.applicant.save()

        appl_props = self.applicant.committee_properties.first()
        appl_props.active_status = APPLICANT_STATUS_ACTIVE
        appl_props.save()

        self.offer_sent = gen_offer_sent(
            offer=self.offer,
            application=self.application
        )
        self.offer_sent.response = True
        self.offer_sent.save()

        self.url = reverse('close_offer-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def test_close_offer(self):
        """Test that we can close offer."""
        self.admin_login()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
            'assigned_application_pk': self.application.pk,
            'message_for_applicant': "You've got mail!",
            'message_for_buildingadministrator': 'All your bases are belong',
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.offer.status, Offer.STATUS_CLOSED)
        self.assertEqual(response.data, {})

    def test_wrong_status(self):
        """Test status finished is required to close."""
        self.admin_login()

        self.offer.status = Offer.STATUS_ABORTED
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
            'assigned_application_pk': self.application.pk,
            'message_for_applicant': "You've got mail!",
            'message_for_buildingadministrator': 'All your bases are belong',
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_ABORTED)
        self.assertEqual(
            response.data['offer_pk'],
            ['Can only close offers, with status finished.']
        )

    def test_reply_is_no(self):
        """Test assignment only allowed when applicant responded yes."""
        self.admin_login()

        self.offer_sent.response = False
        self.offer_sent.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
            'assigned_application_pk': self.application.pk,
            'message_for_applicant': "You've got mail!",
            'message_for_buildingadministrator': 'All your bases are belong',
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_FINISHED)
        self.assertEqual(
            response.data['non_field_errors'],
            ['Can only assign to accepted applications.']
        )

    def test_no_offer_sent(self):
        """Test we cannot assign to someone who did not receive the offer."""
        self.admin_login()

        self.offer_sent.delete()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
            'assigned_application_pk': self.application.pk,
            'message_for_applicant': "You've got mail!",
            'message_for_buildingadministrator': 'All your bases are belong',
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_FINISHED)
        self.assertTrue(
            "Can only assign to applications which" in
            response.data['non_field_errors'][0],
        )

    def test_cant_recieve_offer(self):
        """Test we cannot assign to someone who cannot receive the offer."""
        self.admin_login()

        for applicant in self.application.applicants.all():
            applicant.trigger_default_quarantine(self.offer.tenancy)

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
            'assigned_application_pk': self.application.pk,
            'message_for_applicant': "You've got mail!",
            'message_for_buildingadministrator': 'All your bases are belong',
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_FINISHED)
        self.assertEqual(
            response.data['non_field_errors'],
            ["No applicants can recieve an offer"]
        )


class FinishOfferTest(CreateAdminMixin, APITestCase):
    """Unit-tests for finish_offer-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        self.admin_user = self.create_admin_user()

        self.tenancy = gen_tenancy()

        self.offer = gen_offer(
            status=Offer.STATUS_OPEN,
            tenancy=self.tenancy
        )
        self.offer.save()

        from webapp.models.gen import gen_education
        from webapp.models.util import EDU_STATUS_IN_PROGRESS
        from webapp.models.util import APPLICANT_STATUS_ACTIVE

        self.application = gen_application(
            appl_target=self.tenancy,
        )
        self.applicant = self.application.applicants.first()

        self.applicant.educations.all().delete()
        self.applicant.save()
        gen_education(self.applicant, status=EDU_STATUS_IN_PROGRESS)
        self.applicant.save()

        appl_props = self.applicant.committee_properties.first()
        appl_props.active_status = APPLICANT_STATUS_ACTIVE
        appl_props.save()

        self.offer_sent = gen_offer_sent(
            offer=self.offer,
            application=self.application
        )

        self.url = reverse('finish_offer-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def test_finish_offer(self):
        """Test that we can update offer to finished."""
        self.admin_login()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.offer.status, Offer.STATUS_FINISHED)
        self.assertEqual(response.data, {})

    def test_wrong_status(self):
        """Test that we cannot finish an aborted offer."""
        self.admin_login()

        self.offer.status = Offer.STATUS_ABORTED
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_ABORTED)
        self.assertEqual(
            response.data['offer_pk'],
            ['Can only finish offers, with status open.']
        )


class AbortOfferTest(CreateAdminMixin, APITestCase):
    """Unit-tests for abort offer endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        self.admin_user = self.create_admin_user()

        self.tenancy = gen_tenancy()

        self.offer = gen_offer(
            status=Offer.STATUS_OPEN,
            tenancy=self.tenancy
        )
        self.offer.save()

        from webapp.models.gen import gen_education
        from webapp.models.util import EDU_STATUS_IN_PROGRESS
        from webapp.models.util import APPLICANT_STATUS_ACTIVE

        self.application = gen_application(
            appl_target=self.tenancy,
        )
        self.applicant = self.application.applicants.first()

        self.applicant.educations.all().delete()
        self.applicant.save()
        gen_education(self.applicant, status=EDU_STATUS_IN_PROGRESS)
        self.applicant.save()

        appl_props = self.applicant.committee_properties.first()
        appl_props.active_status = APPLICANT_STATUS_ACTIVE
        appl_props.save()

        self.offer_sent = gen_offer_sent(
            offer=self.offer,
            application=self.application
        )

        self.url = reverse('abort_offer-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    @parameterized.expand([
        [Offer.STATUS_OPEN],
        [Offer.STATUS_EDITING],
    ])
    def test_finish_offer(self, offer_status):
        """Test that we can abort offer."""
        self.admin_login()

        self.offer.status = offer_status
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk,
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.offer.status, Offer.STATUS_ABORTED)
        self.assertEqual(response.data, {})

    def test_wrong_status(self):
        """Test that we cannot abort offer that is already aborted."""
        self.admin_login()

        self.offer.status = Offer.STATUS_ABORTED
        self.offer.save()

        response = self.client.post(self.url, {
            'offer_pk': self.offer.pk
        })
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.offer.status, Offer.STATUS_ABORTED)
        self.assertTrue(
            'Can only abort offers, with status editing, open or' in
            response.data['offer_pk'][0]
        )


class UserOfferTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-test for Offers endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_applicant_user()
        self.url = reverse('offer-list')

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

    def test_reject_not_logged_in(self):
        """Attempting to get without being logged in fails."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"detail": "Authentication credentials were not provided."}
        )

    @parameterized.expand([
        [False, 1],
        [True, 2],
    ])
    def test_allow_get(self, is_admin_user, result_count):
        """Test whether users can get content."""

        offer = gen_offer()
        gen_offer()
        application = gen_application()

        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()
            application = gen_application(applicants=[self.user.applicant])

        gen_offer_sent(application=application, offer=offer)

        data = self.client.get(self.url).data
        self.assertEqual(data['count'], result_count)
        self.assertEqual(data['results'][0]['pk'], offer.pk)

    def test_no_user_passed(self):
        """Test get_queryset_for_user with no user"""

        queryset = OfferViewSet.get_queryset_for_user()
        self.assertTrue(len(queryset) == 0)
