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

from webapp.models import MessageContent
from webapp.models import MessageThread
from webapp.models import util


# pylint: disable=too-many-instance-attributes
class MessageThreadTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the Message Thread api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.user = self.create_applicant_user()
        self.admin_user = self.create_admin_user()
        # Send message
        from webapp.models.gen import gen_message
        from webapp.models.gen import gen_applicant
        from core.util import get_user_message_admin
        self.message1 = gen_message(self.user, self.admin_user)
        self.applicant_user = gen_applicant().user
        self.message2 = gen_message(get_user_message_admin(),
                                    self.applicant_user)
        # urls
        self.non_ordered_list_url = reverse('messagethread-list')
        self.list_url = (reverse('messagethread-list') +
                         "?order_by=-last_activity")
        self.detail_url1 = reverse(
            'messagethread-detail',
            args=[self.message1.messages.first().thread.pk]
        )
        self.detail_url2 = reverse(
            'messagethread-detail',
            args=[self.message2.messages.first().thread.pk]
        )
        # no detail url exists here
        self.assertEqual(MessageContent.objects.count(), 2)
        self.assertEqual(MessageThread.objects.count(), 2)

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
        [lambda self: self.non_ordered_list_url],
        [lambda self: self.list_url],
        [lambda self: self.detail_url1],
        [lambda self: self.detail_url2],
    ])
    def test_X_reject_not_logged_in(self, url_function):
        """Attempting to get without being logged in fails."""
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
    def test_detail_accept_logged_in(self, is_admin_user):
        """Test that the message thread details shows up as expected."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.detail_url1)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['pk'],
                         self.message1.messages.first().thread.pk)
        self.assertEqual(response.data['subject'], 'We talk about stuff')
        self.assertEqual(response.data['last_message_pk'],
                         self.message1.messages.first().pk)
        self.assertEqual("status" in response.data,
                         is_admin_user)

    @parameterized.expand([
        [False, 1],
        [True, 2],
    ])
    def test_list_accept_logged_in(self, is_admin_user, expected):
        """Test that the message thread list shows up as expected."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        # Test we get 2 users back
        self.assertEqual(response.data['count'], expected)
        self.assertEqual(len(response.data['results']), expected)
        self.assertEqual(response.data['next'], None)

    def test_detail_user_can_only_see_own(self):
        """Test that the message thread details shows up as expected."""
        self.user_login()

        response = self.client.get(self.detail_url2)
        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.data, {"detail": "Not found."})

    def test_detail_message_admin_only(self):
        """Test that only_message_admin is set, when expected.

        Namely when no other admin, has send a message in the thread.
        """
        self.admin_login()

        response = self.client.get(self.detail_url2)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['pk'],
                         self.message2.messages.first().thread.pk)
        self.assertEqual(response.data['subject'], 'We talk about stuff')
        self.assertEqual(response.data['last_message_pk'],
                         self.message2.messages.first().pk)
        self.assertEqual("status" in response.data, True)

    @parameterized.expand([
        [False, lambda self: self.list_url],
        [False, lambda self: self.detail_url1],
        [True, lambda self: self.list_url],
        [True, lambda self: self.detail_url1],
    ])
    def test_post_disallowed(self, is_admin_user, url_function):
        """Post requests are always rejected, only PUT and PATCH are ok."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.post(url_function(self))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data,
                         {"detail": "Method \"POST\" not allowed."})

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_setting_status(self, is_admin_user):
        """Only admins can change the status of threads."""
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.patch(self.detail_url1,
                                     {"status": "no_action_needed"})
        thread = self.message1.messages.first().thread
        thread.refresh_from_db()
        if is_admin_user:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data,
                             {"status": "no_action_needed"})
            self.assertEqual(thread.status, "no_action_needed")
        else:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data,
                             {"status": ["Only staff can update status."]})
            self.assertEqual(thread.status,
                             util.MESSAGE_STATUS_NOT_PROCESSED)
