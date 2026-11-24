"""payments: Payment, Refund (docs/05-database-design.md).

Payment is OneToOne with Order — no retry-attempt modeling (confirmed
decision: a failed attempt updates this same row's status rather than
creating a new row).
"""

from django.db import models

from apps.common.models import BaseModel
from apps.orders.models import Order, VendorSubOrder


class Payment(BaseModel):
    class Method(models.TextChoices):
        CARD = "card", "Card"
        UPI = "upi", "UPI"
        NETBANKING = "netbanking", "Netbanking"
        WALLET = "wallet", "Wallet"

    class Status(models.TextChoices):
        INITIATED = "initiated", "Initiated"
        AUTHORIZED = "authorized", "Authorized"
        CAPTURED = "captured", "Captured"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"
        PARTIALLY_REFUNDED = "partially_refunded", "Partially refunded"

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="payment")
    gateway = models.CharField(max_length=50)
    gateway_payment_id = models.CharField(max_length=255, unique=True)
    method = models.CharField(max_length=20, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIATED)
    raw_gateway_response = models.JSONField(default=dict, blank=True)


class Refund(BaseModel):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PROCESSED = "processed", "Processed"

    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="refunds")
    vendor_sub_order = models.ForeignKey(
        VendorSubOrder, on_delete=models.PROTECT, related_name="refunds"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
