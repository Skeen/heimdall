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

from webapp.models.gen import gen_applicant

from webapp.models import MessageContent
from webapp.models import Message
from webapp.models import MessageThread
from webapp.models import util


class MessageSendingTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the Message Sending api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.user = self.create_applicant_user()
        self.admin_user = self.create_admin_user()
        # urls
        self.list_url = reverse('send_message-list')
        # no detail url exists here
        self.assertEqual(MessageContent.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageThread.objects.count(), 0)

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
    def test_reject_get(self, is_admin_user):
        """Attempting to get always fails."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.data,
            {"detail": 'Method "GET" not allowed.'}
        )

    def test_reject_empty_post(self):
        """Attempting to send using empty post fails."""
        # TODO: Test incrementally rejections, i.e. providing one field
        self.user_login()

        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "content": ["This field is required."],
                "subject": ["This field is required."],
                "recievers": ["This field is required."],
            }
        )
        self.assertEqual(MessageContent.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageThread.objects.count(), 0)

    @parameterized.expand([
        [False, util.MESSAGE_STATUS_NOT_PROCESSED],
        [True, util.MESSAGE_STATUS_ANSWERED],
    ])
    def test_send_message(self, is_admin_user, thread_status):
        """It is possible to send a message."""
        if is_admin_user:
            sender = self.admin_user
            reciever = self.user
            self.admin_login()
        else:
            sender = self.user
            reciever = self.admin_user
            self.user_login()

        response = self.client.post(
            self.list_url,
            {
                "content": "Please give me a tenancy!",
                "subject": "Super urgent",
                "recievers": [reciever.pk],
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['thread_pk'],
                         MessageThread.objects.first().pk)
        self.assertEqual(response.data['content'], 'Please give me a tenancy!')
        self.assertEqual(response.data['sender_pk'], sender.pk)
        self.assertEqual(response.data['subject'], 'Super urgent')
        self.assertEqual(MessageContent.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(MessageThread.objects.count(), 1)
        self.assertEqual(MessageThread.objects.first().status, thread_status)

    def test_send_message_no_recievers(self):
        """Attempting to send to no reciever fails."""
        self.user_login()

        response = self.client.post(
            self.list_url,
            {
                "content": "Please give me a tenancy!",
                "subject": "Super urgent",
                "recievers": [],
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,
                         ["Message need atleast 1 reciever."])
        self.assertEqual(MessageContent.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageThread.objects.count(), 0)

    def test_send_message_invalid_reciever(self):
        """Attempting to send to a non-existing reciever fails."""
        self.user_login()

        response = self.client.post(
            self.list_url,
            {
                "content": "Please give me a tenancy!",
                "subject": "Super urgent",
                "recievers": [4242],
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {"recievers": ["Could not lookup all message recipients."]}
        )
        self.assertEqual(MessageContent.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageThread.objects.count(), 0)

    def test_broadcast_message(self):
        """It is possible to boardcast a message."""
        sender = self.admin_user
        recievers = [self.user.pk, gen_applicant().user.pk]
        self.admin_login()

        response = self.client.post(
            self.list_url,
            {
                "content": "You guys are in trouble!",
                "subject": "Super urgent",
                "recievers": recievers,
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['thread_pk'], None)
        self.assertEqual(response.data['content'], 'You guys are in trouble!')
        self.assertEqual(response.data['sender_pk'], sender.pk)
        self.assertEqual(response.data['subject'], 'Super urgent')
        self.assertEqual(response.data['message_pk'], None)
        self.assertEqual(MessageContent.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(MessageThread.objects.count(), 2)

    @parameterized.expand([
        [False],
        [True],
    ])
    def test_send_message_to_running_thread(self, is_admin_user):
        """It is possible to send to an active thread."""
        if is_admin_user:
            sender = self.admin_user
            reciever = self.user
            self.admin_login()
        else:
            sender = self.user
            reciever = self.admin_user
            self.user_login()

        from webapp.models.gen import gen_message
        message = gen_message(self.user, self.admin_user)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(MessageThread.objects.count(), 1)
        response = self.client.post(
            self.list_url,
            {
                "content": "Please give me a tenancy!",
                "subject": "Super urgent",
                "thread": message.messages.first().thread.pk,
                "recievers": [reciever.pk]
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['thread_pk'],
                         MessageThread.objects.first().pk)
        self.assertEqual(response.data['content'], 'Please give me a tenancy!')
        self.assertEqual(response.data['sender_pk'], sender.pk)
        self.assertEqual(response.data['subject'], 'Super urgent')
        self.assertEqual(MessageContent.objects.count(), 2)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(MessageThread.objects.count(), 1)

    def test_send_message_invalid_thread(self):
        """Attempting to send to a non-existing thread fails."""
        self.admin_login()

        response = self.client.post(
            self.list_url,
            {
                "content": "Please give me a tenancy!",
                "subject": "Super urgent",
                "thread": 42,
                "recievers": [self.user.pk]
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,
                         {"thread": ["No such thread found!"]})
        self.assertEqual(MessageContent.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageThread.objects.count(), 0)

    @parameterized.expand([
        [False, 400],
        [True, 201],
    ])
    def test_send_message_hijack_thread(self, is_admin_user, status):
        """Test whether the user can hijack a thread.

        Admins can do this, while ordinary users cannot.

        Hijacking is entering into a thread they do not already participate in.
        """
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        from webapp.models.gen import gen_message
        from core.util import get_user_message_admin
        applicant_user = gen_applicant().user
        message = gen_message(applicant_user, get_user_message_admin())

        self.assertEqual(MessageContent.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(MessageThread.objects.count(), 1)
        response = self.client.post(
            self.list_url,
            {
                "content": "Please give me a tenancy!",
                "subject": "Super urgent",
                "thread": message.messages.first().thread.pk,
                "recievers": [applicant_user.pk if is_admin_user else
                              get_user_message_admin().pk]
            }
        )
        self.assertEqual(response.status_code, status)
        if status == 400:
            self.assertEqual(response.data, ["Invalid thread!"])
            self.assertEqual(MessageContent.objects.count(), 1)
            self.assertEqual(Message.objects.count(), 1)
            self.assertEqual(MessageThread.objects.count(), 1)
        else:
            self.assertEqual(MessageContent.objects.count(), 2)
            self.assertEqual(Message.objects.count(), 2)
            self.assertEqual(MessageThread.objects.count(), 1)
