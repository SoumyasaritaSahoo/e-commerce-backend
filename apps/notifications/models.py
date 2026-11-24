"""notifications: Notification (docs/05-database-design.md)."""

from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel


class Notification(BaseModel):
    class Type(models.TextChoices):
        ORDER_UPDATE = "order_update", "Order update"
        PROMO = "promo", "Promo"
        PAYOUT = "payout", "Payout"
        SYSTEM = "system", "System"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=Type.choices)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
