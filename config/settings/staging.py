"""Staging settings — mirrors production config against seeded/anonymized data
(docs/11-deployment-infra.md)."""

from .base import *  # noqa: F401,F403

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
