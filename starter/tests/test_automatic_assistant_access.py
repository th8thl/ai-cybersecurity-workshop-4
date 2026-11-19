"""Signed-in workshop users can use the assistant without a consent step."""
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone
from chatbot.models import MCPAccessGrant
from security.mcp_authorization import COOKIE_NAME, PERMISSIONS, validate_token
from tickets.models import Ticket


@override_settings(ASSISTANT_AUTO_ACCESS=True, MCP_TRANSPORT="inprocess-test", NEMO_CHECKS=False,
                   PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class AutomaticAssistantAccessTests(TestCase):
    def setUp(self):
        self.alice = get_user_model().objects.create_user("auto-alice")
        self.bob = get_user_model().objects.create_user("auto-bob")

    def test_anonymous_request_does_not_issue_grant(self):
        self.client.get("/chatbot/")
        self.assertFalse(MCPAccessGrant.objects.exists())

    def test_sign_in_automatically_enables_all_workshop_scopes(self):
        self.client.force_login(self.alice)
        response = self.client.get("/chatbot/")
        token = response.cookies[COOKIE_NAME].value
        grant = validate_token(token, expected_user_id=self.alice.pk)
        self.assertEqual(set(grant.scopes), set(PERMISSIONS))
        self.assertEqual(response.cookies[COOKIE_NAME]["path"], "/")
        self.assertTrue(response.cookies[COOKIE_NAME]["httponly"])
        self.assertContains(response, "Available automatically")
        self.assertNotContains(response, "Authorize assistant")
        self.client.get("/knowledge/")
        self.assertEqual(MCPAccessGrant.objects.count(), 1)

    def test_expired_grant_is_refreshed_without_a_consent_page(self):
        self.client.force_login(self.alice)
        self.client.get("/chatbot/")
        MCPAccessGrant.objects.update(expires_at=timezone.now() - timedelta(seconds=1))
        response = self.client.get("/chatbot/")
        grant = validate_token(response.cookies[COOKIE_NAME].value)
        self.assertGreater(grant.expires_at, timezone.now())

    def test_switching_account_binds_access_to_new_user(self):
        self.client.force_login(self.alice)
        self.client.get("/chatbot/")
        self.client.force_login(self.bob)
        response = self.client.get("/chatbot/")
        grant = validate_token(response.cookies[COOKIE_NAME].value)
        self.assertEqual(grant.user_id, self.bob.pk)

    def test_ticket_ownership_still_applies(self):
        ticket = Ticket.objects.create(owner=self.bob, title="Bob private ticket")
        self.client.force_login(self.alice)
        response = self.client.get(f"/tickets/{ticket.pk}/")
        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, "Bob private ticket", status_code=404)

    def test_separate_browser_sessions_do_not_revoke_each_other(self):
        from django.test import Client
        other = Client()
        self.client.force_login(self.alice)
        other.force_login(self.alice)
        first = self.client.get("/chatbot/").cookies[COOKIE_NAME].value
        second = other.get("/chatbot/").cookies[COOKIE_NAME].value
        self.assertEqual(first, second)
        self.assertEqual(validate_token(first).user_id, self.alice.pk)
        self.assertEqual(validate_token(second).user_id, self.alice.pk)

    def test_mcp_ticket_access_works_on_first_signed_in_request(self):
        from django.test import RequestFactory
        from django.http import JsonResponse
        from chatbot.mcp_client import call, discover
        from security.mcp_authorization import MCPAuthorizationMiddleware
        own = Ticket.objects.create(owner=self.alice, title="Alice ticket")
        other = Ticket.objects.create(owner=self.bob, title="Bob ticket")
        request = RequestFactory().get("/chatbot/")
        request.user = self.alice

        def view(request):
            names = {item["name"] for item in discover(request.user)["tools"]}
            self.assertIn("search_knowledge", names)
            result = call(request.user, "get_ticket", {"ticket_id": own.pk})
            self.assertEqual(result["ticket_id"], own.pk)
            with self.assertRaises(PermissionError):
                call(request.user, "get_ticket", {"ticket_id": other.pk})
            return JsonResponse({"ok": True})

        response = MCPAuthorizationMiddleware(view)(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(COOKIE_NAME, response.cookies)
