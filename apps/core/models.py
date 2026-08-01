"""Shared base models used across apps (docs/10-project-structure.md)."""

import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base adding created/updated timestamps to any model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base for models that need a public-facing UUID identifier
    separate from the internal auto-incrementing primary key."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class AuditLog(TimeStampedModel):
    """Generic audit trail for sensitive actions (admin approvals, refunds,
    payout decisions, etc.) across any app."""

    actor_id = models.PositiveBigIntegerField(null=True, blank=True)
    action = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100)
    target_id = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} on {self.target_type}#{self.target_id}"
