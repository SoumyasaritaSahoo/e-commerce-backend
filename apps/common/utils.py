"""Generic utility functions shared across apps."""

import secrets


def generate_secure_token(length=32):
    """URL-safe random token — for email verification / password reset
    links (Phase 1.1, docs/14-execution-checklist.md)."""
    return secrets.token_urlsafe(length)
