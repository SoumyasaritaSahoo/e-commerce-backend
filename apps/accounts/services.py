
"""Business logic for accounts, called from views.py."""

import hashlib
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.common.exceptions import ApplicationError
from apps.common.utils import generate_secure_token

from .models import EmailVerificationToken, PasswordResetToken


EMAIL_VERIFICATION_EXPIRY_HOURS = 24
PASSWORD_RESET_EXPIRY_HOURS = 1


def create_email_verification_token(user):
    """
    Create a new email verification token.

    Only the SHA-256 hash is stored in the database.
    Returns the raw token so it can be included in the verification email.
    """
    now = timezone.now()

    # Invalidate all previous unused tokens for this user.
    EmailVerificationToken.objects.filter(
        user=user,
        used_at__isnull=True,
    ).update(used_at=now)

    raw_token = generate_secure_token()
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    EmailVerificationToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=now + timedelta(hours=EMAIL_VERIFICATION_EXPIRY_HOURS),
    )

    return raw_token


@transaction.atomic
def verify_email_verification_token(raw_token):
    """
    Validate and consume an email verification token.

    Returns the verified user.
    Raises ApplicationError if the token is invalid, expired, or already used.
    """
    if not raw_token:
        raise ApplicationError(
            detail="Invalid or expired verification link.",
            code="invalid_or_expired_verification_token",
        )

    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    verification_token = (
        EmailVerificationToken.objects.select_for_update()
        .filter(
            token_hash=token_hash,
            used_at__isnull=True,
            expires_at__gt=timezone.now(),
        )
        .select_related("user")
        .first()
    )

    if verification_token is None:
        raise ApplicationError(
            detail="Invalid or expired verification link.",
            code="invalid_or_expired_verification_token",
        )

    now = timezone.now()

    verification_token.used_at = now
    verification_token.save(update_fields=["used_at", "updated_at"])

    user = verification_token.user

    if not user.is_email_verified:
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

    return user


def create_password_reset_token(user):
    """
    Create a new password reset token.

    Only the SHA-256 hash is stored in the database.
    Returns the raw token so it can be included in the reset email.
    """
    now = timezone.now()

    # Invalidate all previous unused tokens for this user.
    PasswordResetToken.objects.filter(
        user=user,
        used_at__isnull=True,
    ).update(used_at=now)

    raw_token = generate_secure_token()
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    PasswordResetToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=now + timedelta(hours=PASSWORD_RESET_EXPIRY_HOURS),
    )

    return raw_token


@transaction.atomic
def reset_password(raw_token, new_password):
    """
    Validate and consume a password reset token, setting the user's new
    password.

    Raises ApplicationError if the token is invalid, expired, or already used.
    """
    if not raw_token:
        raise ApplicationError(
            detail="Invalid or expired reset link.",
            code="invalid_or_expired_reset_token",
        )

    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    reset_token = (
        PasswordResetToken.objects.select_for_update()
        .filter(
            token_hash=token_hash,
            used_at__isnull=True,
            expires_at__gt=timezone.now(),
        )
        .select_related("user")
        .first()
    )

    if reset_token is None:
        raise ApplicationError(
            detail="Invalid or expired reset link.",
            code="invalid_or_expired_reset_token",
        )

    reset_token.used_at = timezone.now()
    reset_token.save(update_fields=["used_at", "updated_at"])

    user = reset_token.user
    user.set_password(new_password)
    user.save(update_fields=["password"])

    return user
