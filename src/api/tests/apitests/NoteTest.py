"""Unit-tests for api.views

Todo:
    Refactor logged-in required redirects as mixin.
"""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^
# pylint: disable=no-member
from rest_framework.test import APITestCase
from django.urls import reverse

from adminapp.tests.viewtests.util import CreateAdminMixin
from webapp.tests.viewtests.util import CreateUserMixin

from webapp.models import Note


class NoteTest(CreateAdminMixin, CreateUserMixin, APITestCase):
    """Unit-tests for note-list and attach_offer_note-list."""

    def setUp(self):
        CreateAdminMixin.setup(self)
        CreateUserMixin.setup(self)
        self.admin_user = self.create_admin_user()
        self.user = self.create_applicant_user()

        self.url = reverse('note-list')
        self.attach_url = reverse('attach_offer_note-list')

    def admin_login(self):
        """Login the admin user."""
        logged_in = self.client.login(username=self.adminlogin['username'],
                                      password=self.adminlogin['password'])
        self.assertTrue(logged_in)

    def test_create_note(self):
        """Test that we can create notes."""
        self.admin_login()

        text = 'NOTE TEXT HERE'
        self.assertEqual(Note.objects.count(), 0)
        response = self.client.post(self.url, {
            'text': text,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().text, text)

    def test_attach_to_offer(self):
        """Test that a note can be attached to an offer."""
        from webapp.models.gen.Offer import gen_offer
        offer = gen_offer()

        self.test_create_note()
        note = Note.objects.first()
        self.assertEqual(offer.notes.count(), 0)
        response = self.client.post(self.attach_url, {
            'note_pk': note.pk,
            'offer_pk': offer.pk,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(offer.notes.count(), 1)
        self.assertEqual(offer.notes.first(), note)
