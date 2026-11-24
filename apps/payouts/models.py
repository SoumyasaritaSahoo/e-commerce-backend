"""payouts: Payout, PayoutItem (docs/05-database-design.md)."""

from django.db import models

from apps.common.models import BaseModel
from apps.orders.models import VendorSubOrder
from apps.vendors.models import VendorStore


class Payout(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    vendor_store = models.ForeignKey(VendorStore, on_delete=models.PROTECT, related_name="payouts")
    period_start = models.DateField()
    period_end = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    bank_reference = models.CharField(max_length=255, null=True, blank=True)


class PayoutItem(BaseModel):
    payout = models.ForeignKey(Payout, on_delete=models.CASCADE, related_name="items")
    vendor_sub_order = models.ForeignKey(
        VendorSubOrder, on_delete=models.PROTECT, related_name="payout_items"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
