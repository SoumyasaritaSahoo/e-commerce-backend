"""Local development settings — Docker Compose stack, MinIO, verbose errors."""

from .base import *  # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# Local MinIO stands in for S3 (docs/11-deployment-infra.md).
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="http://minio:9000")  # noqa: F405
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
