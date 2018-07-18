"""Unit-tests for api.views

Todo:
    Refactor logged-in required redirects as mixin.
"""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils.encoding import smart_text
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin

from webapp.models import MessageContent
from webapp.models import Message
from webapp.models import MessageThread

from webapp.models.gen import gen_message
from webapp.models.gen import gen_applicant
from core.util import get_user_message_admin


# pylint: disable=too-many-instance-attributes
class MessageRecipientTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for the MessageRecipient api endpoint."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.user = self.create_applicant_user()
        self.admin_user = self.create_admin_user()
        # Send message
        self.message1 = gen_message(self.user, self.admin_user)
        self.applicant_user = gen_applicant().user
        self.message2 = gen_message(get_user_message_admin(),
                                    self.applicant_user)
        # urls
        self.list_url = reverse('message-list')
        self.detail_url1 = reverse('message-detail',
                                   args=[self.message1.messages.first().pk])
        self.detail_url2 = reverse('message-detail',
                                   args=[self.message2.messages.first().pk])
        # no detail url exists here
        self.assertEqual(MessageContent.objects.count(), 2)
        self.assertEqual(Message.objects.count(), 2)
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
        """Test that the message details shows up as expected."""
        # Login
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.get(self.detail_url1)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['pk'],
                         self.message1.messages.first().pk)
        self.assertEqual(response.data['subject'],
                         self.message1.subject)
        self.assertEqual(response.data['content'],
                         self.message1.content)
        self.assertEqual(response.data['sender']['pk'],
                         self.message1.sender.pk)
        self.assertEqual(response.data['read'],
                         False if is_admin_user else None)

    @parameterized.expand([
        [False, 1],
        [True, 2],
    ])
    def test_list_accept_logged_in(self, is_admin_user, expected):
        """Test that the message list shows up as expected."""
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

    def test_filter_user_pk(self):
        """Test that the message list shows up as expected."""
        self.admin_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)

        response = self.client.get(
            self.list_url + "?user_pk=" + smart_text(self.user.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['next'], None)

    def test_filter_sender(self):
        """Test that the message list shows up as expected."""
        self.admin_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)

        response = self.client.get(
            self.list_url + "?sender=" + smart_text(self.user.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['next'], None)

        gen_message(self.user, self.admin_user)
        response = self.client.get(
            self.list_url + "?sender=" + smart_text(self.user.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)

    def test_filter_recipient(self):
        """Test that the message list shows up as expected."""
        self.admin_login()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)

        response = self.client.get(
            self.list_url + "?recipient=" + smart_text(self.user.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.data['next'], None)

        gen_message(self.admin_user, self.user)

        response = self.client.get(
            self.list_url + "?recipient=" + smart_text(self.user.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['next'], None)

    def test_filter_thread_pk(self):
        """Test that the message list shows up as expected."""
        self.admin_login()

        thread = self.message1.messages.first().thread

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)

        response = self.client.get(
            self.list_url + "?thread_pk=" + smart_text(thread.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['next'], None)

        message = MessageContent.objects.create(
            sender=self.user,
            subject="HI",
            content="BYE")
        message.send([get_user_message_admin()], thread=thread)

        response = self.client.get(
            self.list_url + "?thread_pk=" + smart_text(thread.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['next'], None)

    def test_detail_user_can_only_see_own(self):
        """Test that the message details shows up as expected."""
        self.user_login()

        response = self.client.get(self.detail_url2)
        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.data, {"detail": "Not found."})

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
    def test_setting_read_status(self, is_admin_user):
        """Only admins can change the read status of messages."""
        if is_admin_user:
            self.admin_login()
        else:
            self.user_login()

        response = self.client.patch(self.detail_url1,
                                     {"read": True})

        self.message1.refresh_from_db()
        if is_admin_user:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data,
                             {"read": True})
            self.assertEqual(self.message1.messages.first().read, True)
        else:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.data,
                {"read": ["Non staff, can't update other peoples read field."]}
            )
            self.assertEqual(self.message1.messages.first().read, False)

    def test_read_cannot_be_set_false(self):
        """Message cannot be set as unread."""
        self.admin_login()

        message = self.message1.messages.first()
        message.read = True
        message.save()

        response = self.client.patch(self.detail_url1,
                                     {"read": False})

        message.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,
                         {"read": ['Read can only be set to true.']})
        self.assertEqual(message.read, True)

    def test_users_can_set_read_on_message_they_receive(self):
        """Users can set their own messages as read."""
        self.user_login()

        message3 = gen_message(self.admin_user, self.user)
        detail_url3 = reverse('message-detail',
                              args=[message3.messages.first().pk])

        response = self.client.patch(detail_url3,
                                     {"read": True})

        message3.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         {"read": True})
        self.assertEqual(message3.messages.first().read, True)
