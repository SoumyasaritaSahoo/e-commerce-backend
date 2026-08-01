"""Reusable file/field validators.

Password rules are NOT here — they already come from
AUTH_PASSWORD_VALIDATORS (config/settings/base.py); duplicating them here
would create a second, driftable source of truth.

Size/MIME thresholds below are this project's own defaults, since
docs/08-security-plan.md requires server-side MIME+size validation on
uploads but doesn't specify the numbers — adjust when a concrete app
(catalog product images, vendor documents) wires these in.
"""

from django.core.exceptions import ValidationError

ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def validate_file_size(max_mb):
    def _validate(file):
        max_bytes = max_mb * 1024 * 1024
        if file.size > max_bytes:
            raise ValidationError(f"File must be {max_mb}MB or smaller.")

    return _validate


def validate_image_content_type(file):
    content_type = getattr(file, "content_type", None)
    if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_CONTENT_TYPES))
        raise ValidationError(f"Unsupported image type: {content_type}. Allowed: {allowed}.")
