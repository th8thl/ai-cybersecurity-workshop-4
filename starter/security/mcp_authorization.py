"""Workshop consent and opaque delegated tokens; this is not an OAuth provider."""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import timedelta
import hashlib
import secrets
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.contrib.auth import get_user_model
from chatbot.models import MCPAccessGrant

CLIENT_ID = 'support_portal_assistant'
CLIENT_NAME = 'Support portal assistant'
AUDIENCE = 'support_portal_mcp'
COOKIE_NAME = 'mcp_access_token'
PERMISSIONS = {
    'knowledge:read': 'Search my permitted knowledge base',
    'tickets:read': 'Read my tickets',
    'tickets:create': 'Create tickets for my account',
    'tickets:propose-close': 'Request closure of my tickets',
}
TOOL_SCOPES = {'search_knowledge':'knowledge:read', 'list_tickets':'tickets:read', 'get_ticket':'tickets:read',
               'create_ticket':'tickets:create', 'close_ticket':'tickets:propose-close'}
_access_token = ContextVar('mcp_access_token', default=None)


class MCPAuthorizationError(PermissionError):
    def __init__(self, message, code='authorization_required'):
        super().__init__(message)
        self.code = code


def token_digest(token):
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


@contextmanager
def use_access_token(token):
    context = _access_token.set(token)
    try:
        yield
    finally:
        _access_token.reset(context)


def current_access_token():
    return _access_token.get()


def issue_grant(user, scopes, lifetime_seconds=1800):
    scopes = sorted(set(scopes))
    if not user.is_active or not scopes or not set(scopes) <= set(PERMISSIONS):
        raise ValueError('Choose at least one of the listed permissions.')
    if lifetime_seconds not in {60, 300, 1800}:
        raise ValueError('Choose an authorization duration from the list.')
    raw_token = 'mcp_' + secrets.token_urlsafe(32)
    with transaction.atomic():
        MCPAccessGrant.objects.filter(user=user, client_id=CLIENT_ID, revoked_at__isnull=True).update(revoked_at=timezone.now())
        grant = MCPAccessGrant.objects.create(user=user, client_id=CLIENT_ID,
            audience=AUDIENCE, token_hash=token_digest(raw_token), scopes=scopes,
            expires_at=timezone.now()+timedelta(seconds=lifetime_seconds))
    return grant, raw_token


def validate_token(raw_token, scope=None, expected_user_id=None):
    if not isinstance(raw_token,str) or not raw_token.startswith('mcp_') or len(raw_token)>128:
        raise MCPAuthorizationError('Authorize the assistant before it can use your tickets.')
    grant = MCPAccessGrant.objects.select_related('user').filter(token_hash=token_digest(raw_token)).first()
    if grant is None:
        raise MCPAuthorizationError('This access token is not valid. Authorize the assistant again.')
    if grant.client_id != CLIENT_ID or grant.audience != AUDIENCE:
        raise MCPAuthorizationError('This token was not issued for this assistant and MCP server.', 'wrong_client')
    if grant.revoked_at is not None:
        raise MCPAuthorizationError('Assistant access was revoked. Authorize it again to reconnect.', 'authorization_revoked')
    if grant.expires_at <= timezone.now():
        raise MCPAuthorizationError('Assistant access expired. Authorize it again to reconnect.', 'authorization_expired')
    if not grant.user.is_active or (expected_user_id is not None and grant.user_id != expected_user_id):
        raise MCPAuthorizationError('This authorization does not belong to the signed-in account.', 'wrong_user')
    if scope is not None and scope not in grant.scopes:
        label = PERMISSIONS.get(scope,scope)
        raise MCPAuthorizationError(f'You have not authorized this permission: {label}. Use Manage assistant access to change it.', 'insufficient_permission')
    return grant


def require_authorization(user, scope=None):
    return validate_token(current_access_token(), scope, expected_user_id=user.pk)


def authorization_status(user):
    if not current_access_token():
        latest = MCPAccessGrant.objects.filter(user=user,client_id=CLIENT_ID).order_by('-created_at').first()
        if latest and latest.revoked_at is not None:
            return None, 'Assistant access was revoked. Authorize it again to reconnect.'
        if latest and latest.expires_at <= timezone.now():
            return None, 'Assistant access expired. Authorize it again to reconnect.'
        return None, 'Authorize the assistant before it can use your tickets.'
    try:
        return require_authorization(user), None
    except MCPAuthorizationError as exc:
        return None, str(exc)


def revoke_grants(user):
    return MCPAccessGrant.objects.filter(user=user,client_id=CLIENT_ID,revoked_at__isnull=True).update(revoked_at=timezone.now())


def automatic_access_token(user):
    """Reuse the user's workshop grant across signed-in browser sessions."""
    with transaction.atomic():
        get_user_model().objects.select_for_update().get(pk=user.pk)
        grant = MCPAccessGrant.objects.filter(
            user=user, client_id=CLIENT_ID, revoked_at__isnull=True,
        ).first()
        if grant is None or grant.audience != AUDIENCE or grant.expires_at <= timezone.now():
            grant, _ = issue_grant(user, PERMISSIONS)
        token = "mcp_" + salted_hmac("session4-assistant-access", str(grant.pk)).hexdigest()
        grant.token_hash = token_digest(token)
        grant.scopes = sorted(PERMISSIONS)
        grant.save(update_fields=["token_hash", "scopes"])
        return token


class MCPAuthorizationMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get(COOKIE_NAME)
        automatic = getattr(settings, "ASSISTANT_AUTO_ACCESS", True)
        issued = False
        if automatic and request.user.is_authenticated and request.user.is_active:
            try:
                grant = validate_token(token, expected_user_id=request.user.pk)
                if not set(PERMISSIONS).issubset(grant.scopes):
                    raise MCPAuthorizationError("Refresh workshop assistant access.")
            except MCPAuthorizationError:
                token = automatic_access_token(request.user)
                issued = True
        with use_access_token(token):
            response = self.get_response(request)
        if automatic and issued and request.user.is_authenticated:
            response.set_cookie(
                COOKIE_NAME, token, max_age=1800, path="/",
                httponly=True, secure=request.is_secure(), samesite="Lax",
            )
            response["Cache-Control"] = "no-store"
        elif automatic and not request.user.is_authenticated and request.COOKIES.get(COOKIE_NAME):
            response.delete_cookie(COOKIE_NAME, path="/")
        return response
