"""The Session 4 portal exposes file operations to authorized users."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from tickets.models import Ticket


class SessionScopeTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('scope-user')
        self.ticket = Ticket.objects.create(owner=user, title='Ordinary ticket')
        self.client.force_login(user)

    def test_file_routes_are_available(self):
        for path in ['/tickets/import/', '/tickets/import/template/',
                     f'/tickets/{self.ticket.pk}/export/']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_ticket_pages_show_file_controls(self):
        listing = self.client.get('/tickets/')
        detail = self.client.get(f'/tickets/{self.ticket.pk}/')
        self.assertContains(detail, 'Ordinary ticket')
        self.assertContains(listing, 'Import a ticket file')
        self.assertContains(detail, 'Upload attachment')
        self.assertContains(detail, 'Export ticket as JSON')
