
"""Asynchronous email tasks for the accounts app."""

from urllib.parse import urlencode

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .services import create_email_verification_token, create_password_reset_token


@shared_task(name="accounts.send_email_verification")
def send_email_verification_email(user_id):
    """
    Generate a verification token and send the email asynchronously.

    Only user_id is passed through the Celery queue.
    The raw token is generated inside the worker.
    """
    User = get_user_model()

    user = User.objects.filter(
        pk=user_id,
        is_active=True,
        is_email_verified=False,
    ).first()

    if user is None:
        return {"status": "skipped", "reason": "user_not_found_or_already_verified"}

    raw_token = create_email_verification_token(user)

    query_string = urlencode({"token": raw_token})
    verification_url = (
        f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?{query_string}"
    )

    send_mail(
        subject="Verify your email address",
        message=(
            f"Hello {user.full_name},\n\n"
            "Thank you for registering. Please verify your email address "
            "using the link below:\n\n"
            f"{verification_url}\n\n"
            "This link expires in 24 hours. If you did not create this "
            "account, you can ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return {"status": "sent", "user_id": user_id}


@shared_task(name="accounts.send_password_reset")
def send_password_reset_email(user_id):
    """
    Generate a password reset token and send the email asynchronously.

    Only user_id is passed through the Celery queue. The raw token is
    generated inside the worker. The requesting view queues this task
    without revealing whether the account exists, so a missing/inactive
    user here is a silent no-op.
    """
    User = get_user_model()

    user = User.objects.filter(pk=user_id, is_active=True).first()

    if user is None:
        return {"status": "skipped", "reason": "user_not_found"}

    raw_token = create_password_reset_token(user)

    query_string = urlencode({"token": raw_token})
    reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?{query_string}"

    send_mail(
        subject="Reset your password",
        message=(
            f"Hello {user.full_name},\n\n"
            "We received a request to reset your password. Use the link "
            "below to choose a new one:\n\n"
            f"{reset_url}\n\n"
            "This link expires in 1 hour. If you did not request a "
            "password reset, you can ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return {"status": "sent", "user_id": user_id}
