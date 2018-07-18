"""Unit-tests for api.views

Todo:
    Refactor logged-in required redirects as mixin.
"""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin

from webapp.models import Applicant
from webapp.models import Application
from webapp.models import ApplicationInvite
from webapp.models.util import APPLICANT_STATUS_HOLD
from webapp.models.gen import gen_applicant
from webapp.models.gen import gen_application_invite
from webapp.models.gen import gen_tenancy_group
from webapp.models.gen import gen_tenancy
from webapp.models.gen import gen_application


# pylint: disable=too-many-instance-attributes
class ApplicationInviteTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for applicationinvite views."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_user()
        self.applicant = gen_applicant(
            user=self.user,
            active_status=APPLICANT_STATUS_HOLD
        )
        self.invite = gen_application_invite(recipient=self.applicant)

        self.applicant2 = gen_applicant(active_status=APPLICANT_STATUS_HOLD)
        self.invite2 = gen_application_invite(recipient=self.applicant2)

        self.test_start_time = timezone.now()

        self.list_url = reverse('applicationinvite-list')
        self.detail_url = reverse(
            'applicationinvite-detail', args=[self.invite.pk]
        )
        self.detail_url2 = reverse(
            'applicationinvite-detail', args=[self.invite2.pk]
        )
        self.delete_url = reverse('remove_co_applicant-list')

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
        [False, 1],
        [True, 2],
    ])
    def test_list_accept_logged_in(self, is_admin_user, expected_items):
        """Test that the applicationinvite list shows up as expected.

        I.e. that a user can only see their own, but admins can see all.
        """
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ApplicationInvite.objects.count(), 2)
        self.assertEqual(response.data['count'], expected_items)
        self.assertEqual(len(response.data['results']), expected_items)
        self.assertEqual(response.data['next'], None)

    def test_list_sender_recipient_filter(self):
        """Test our filters sender/recipient filters work."""
        self.admin_login()

        response = self.client.get(
            self.list_url + "?sender=" + str(self.invite.sender.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ApplicationInvite.objects.count(), 2)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['next'], None)

        response = self.client.get(
            self.list_url + "?recipient=" + str(self.applicant.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ApplicationInvite.objects.count(), 2)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['next'], None)


    def test_list_responded_filter(self):
        """Test that our responded filter works."""
        self.admin_login()

        self.assertEqual(ApplicationInvite.objects.count(), 2)

        resp_dict = {'None': 2, 'False': 2, 'True': 0}
        for key, value in resp_dict.iteritems():
            response = self.client.get(self.list_url + "?responded=" + key)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['count'], value)
            self.assertEqual(len(response.data['results']), value)
            self.assertEqual(response.data['next'], None)

        self.invite.response_time = self.test_start_time
        self.invite.save()

        resp_dict = {'None': 2, 'False': 1, 'True': 1}
        for key, value in resp_dict.iteritems():
            response = self.client.get(self.list_url + "?responded=" + key)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['count'], value)
            self.assertEqual(len(response.data['results']), value)
            self.assertEqual(response.data['next'], None)

    @parameterized.expand([
        [False, lambda self: self.detail_url, True],
        [True, lambda self: self.detail_url, True],
        [False, lambda self: self.detail_url2, False],
        [True, lambda self: self.detail_url2, True],
    ])
    def test_detail_accept_logged_in(self, is_admin_user, url, allowed):
        """Test that the user detail page up as expected.

        I.e. that a user can only see their own, but admins can see all.
        """
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        detail_url = url(self)
        response = self.client.get(detail_url)
        if allowed:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_remove_co_applicant(self, has_co_applicant):
        """Test that users can remomve their co-applicants."""
        self.user_login()

        if has_co_applicant:
            self.applicant.co_applicant = self.applicant2
        else:
            self.applicant.co_applicant = None

        group = gen_tenancy_group()

        # 1 room application
        tenancy1 = gen_tenancy(group=group)
        tenancy1.properties.no_rooms = 1
        tenancy1.properties.children_allowed = False
        tenancy1.properties.save()
        application1 = gen_application(
            appl_target=tenancy1,
            applicants=[self.applicant]
        )

        # 2 room application
        tenancy2 = gen_tenancy(group=group)
        tenancy2.properties.no_rooms = 2
        tenancy1.properties.children_allowed = False
        tenancy2.properties.save()
        application2 = gen_application(
            appl_target=tenancy2,
            applicants=[self.applicant]
        )

        self.assertEqual(self.applicant.applications.count(), 2)
        if has_co_applicant:
            # Check that the co_applicant was automatically added
            self.assertEqual(application1.applicants.count(), 1)
            self.assertEqual(application2.applicants.count(), 2)
        else:
            # Check that no co_applicant was automatically added
            self.assertEqual(application1.applicants.count(), 1)
            self.assertEqual(application2.applicants.count(), 1)

        response = self.client.post(self.delete_url)
        self.applicant.refresh_from_db()
        if has_co_applicant:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.applicant.co_applicant, None)
            # Check that we deleted co-applicant applications
            self.assertEqual(self.applicant.applications.count(), 1)
            application1.refresh_from_db()
            with self.assertRaises(Application.DoesNotExist):
                application2.refresh_from_db()
        else:
            self.assertEqual(response.status_code, 400)
            self.assertTrue(
                "You don't have a coapplicant." in
                response.content
            )

    def test_remove_co_applicant_admin(self):
        """Test that adminapp users cannot post to remove co-applicants."""
        self.admin_login()

        with self.assertRaises(Applicant.DoesNotExist):
            self.client.post(self.delete_url)

    def test_send_invite_success(self):
        """Test that an applicant can invite a co-applicant."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant2.applicant_number
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ApplicationInvite.objects.count(), 3)
        newest = ApplicationInvite.objects.order_by('-created_time').first()
        self.assertEqual(newest.sender, self.applicant)
        self.assertEqual(newest.recipient, self.applicant2)
        self.assertEqual(newest.response, None)
        self.assertEqual(newest.response_time, None)

    def test_send_invite_invalid_number(self):
        """Test that an applicant can invite a co-applicant."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        response = self.client.post(self.list_url, {
            'applicant_number': 'C-3PO+R2D2+42'
        })

        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "applicant_number seems invalid." in
            response.content
        )
        self.assertEqual(ApplicationInvite.objects.count(), 2)

    def test_send_invite_co_applicant(self):
        """Test that an applicant can invite a co-applicant."""
        self.user_login()
        self.applicant.co_applicant = self.applicant2
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant2.applicant_number
        })

        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "You already have a coapplicant." in
            response.content
        )
        self.assertEqual(ApplicationInvite.objects.count(), 2)

    def test_send_invite_self(self):
        """Test that an applicant can invite a co-applicant."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant.applicant_number
        })

        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "You cannot be your own coapplicant." in
            response.content
        )
        self.assertEqual(ApplicationInvite.objects.count(), 2)

    def test_send_invite_twice(self):
        """Test that an applicant can invite a co-applicant."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant2.applicant_number
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ApplicationInvite.objects.count(), 3)
        newest = ApplicationInvite.objects.order_by('-created_time').first()
        self.assertEqual(newest.sender, self.applicant)
        self.assertEqual(newest.recipient, self.applicant2)
        self.assertEqual(newest.response, None)
        self.assertEqual(newest.response_time, None)

        # Cannot resend
        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant2.applicant_number
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "You have already sent a similar invitation." in
            response.content
        )
        self.assertEqual(ApplicationInvite.objects.count(), 3)

        # Unless old one was replied to, then a new should be created
        newest.response = False
        newest.response_time = self.test_start_time
        newest.save()

        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant2.applicant_number
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ApplicationInvite.objects.count(), 4)
        new_newest = ApplicationInvite.objects.order_by('-created_time').first()
        self.assertEqual(new_newest.sender, self.applicant)
        self.assertEqual(new_newest.recipient, self.applicant2)
        self.assertEqual(new_newest.response, None)
        self.assertEqual(new_newest.response_time, None)
        self.assertNotEqual(new_newest.pk, newest.pk)

    def test_send_invite_incoming(self):
        """Test that an applicant can invite a co-applicant."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        gen_application_invite(sender=self.applicant2, recipient=self.applicant)
        self.assertEqual(ApplicationInvite.objects.count(), 3)

        response = self.client.post(self.list_url, {
            'applicant_number': self.applicant2.applicant_number
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "You already have an invite from that person." in
            response.content
        )
        self.assertEqual(ApplicationInvite.objects.count(), 3)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_reply(self, reply):
        """Test that we can reply to an invite."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        self.assertEqual(self.applicant.co_applicant, None)
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        # Reply
        response = self.client.patch(self.detail_url, {
            'response': reply
        })
        self.invite.refresh_from_db()
        # Expect 200, and status change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.invite.response, reply)
        self.assertGreater(self.invite.response_time, self.test_start_time)
        # If reply was True, expect co_applicant to be set
        if reply:
            self.assertEqual(self.applicant.co_applicant, self.invite.sender)
        else:
            self.assertEqual(self.applicant.co_applicant, None)

    def test_reply_only_sender_none(self):
        """Test that only the sender can reply none."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        self.assertEqual(self.applicant.co_applicant, None)
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        # Reply to received invite
        response = self.client.patch(self.detail_url, {
            'response': None
        })
        self.invite.refresh_from_db()
        # Expect 400, error message and no change
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "Only sender can respond with 'None'." in
            response.content
        )
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        sent_invite = gen_application_invite(sender=self.applicant)
        sent_invite_url = reverse(
            'applicationinvite-detail', args=[sent_invite.pk]
        )
        # Reply to sent invite
        response = self.client.patch(sent_invite_url, {
            'response': None
        })
        sent_invite.refresh_from_db()
        # Expect 200, and status change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sent_invite.response, None)
        self.assertGreater(sent_invite.response_time, self.test_start_time)

    def test_reply_only_reciever_not_none(self):
        """Test that only the reciever can reply non-none."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        self.assertEqual(self.applicant.co_applicant, None)
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        sent_invite = gen_application_invite(sender=self.applicant)
        sent_invite_url = reverse(
            'applicationinvite-detail', args=[sent_invite.pk]
        )
        # Reply to sent invite
        response = self.client.patch(sent_invite_url, {
            'response': False
        })
        sent_invite.refresh_from_db()
        # Expect 400, error message and no change
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "Only the recipient can respond to an invite." in
            response.content
        )
        self.assertEqual(sent_invite.response, None)
        self.assertEqual(sent_invite.response_time, None)

        # Reply to received invite
        response = self.client.patch(self.detail_url, {
            'response': False
        })
        self.invite.refresh_from_db()
        # Expect 200, and status change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.invite.response, False)
        self.assertGreater(self.invite.response_time, self.test_start_time)

    def test_reply_reply(self):
        """Test that replying to an already replied invite fails."""
        self.user_login()
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        self.assertEqual(self.applicant.co_applicant, None)
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        # Reply first time
        response = self.client.patch(self.detail_url, {
            'response': False
        })
        self.invite.refresh_from_db()
        # Except 200, and status change
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.invite.response, False)
        self.assertGreater(self.invite.response_time, self.test_start_time)
        response_time = self.invite.response_time

        # Reply second time
        response = self.client.patch(self.detail_url, {
            'response': True
        })
        self.invite.refresh_from_db()
        # Expect 400, error message and no change
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "invite has already been replied to." in
            response.content
        )
        self.assertEqual(self.invite.response, False)
        self.assertEqual(self.invite.response_time, response_time)

    def test_reply_yes_with_recipient_coapplicant(self):
        """Test that replying to an already replied invite fails."""
        self.user_login()
        self.applicant.co_applicant = self.applicant2
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        self.assertEqual(self.applicant.co_applicant, self.applicant2)
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        # Reply
        response = self.client.patch(self.detail_url, {
            'response': True
        })
        self.invite.refresh_from_db()
        # Expect 400, error message and no change
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "You already have a coapplicant." in
            response.content
        )
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

    def test_reply_yes_with_sender_coapplicant(self):
        """Test that replying to an already replied invite fails."""
        self.user_login()
        self.invite.sender.co_applicant = self.applicant2
        self.assertEqual(ApplicationInvite.objects.count(), 2)

        self.assertEqual(self.applicant.co_applicant, None)
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)

        # Reply
        response = self.client.patch(self.detail_url, {
            'response': True
        })
        self.invite.refresh_from_db()
        # Expect 400, error message and no change
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "Sender already has a coapplicant." in
            response.content
        )
        self.assertEqual(self.invite.response, None)
        self.assertEqual(self.invite.response_time, None)
