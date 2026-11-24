"""promotions: Coupon, CouponRedemption (docs/05-database-design.md).

CouponRedemption.order uses a string reference ("orders.Order") — the
circular orders/promotions app dependency (Order.coupon -> Coupon here)
means neither app's models.py is fully self-contained.
"""

from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.vendors.models import VendorStore


class Coupon(BaseModel):
    class Scope(models.TextChoices):
        PLATFORM = "platform", "Platform"
        VENDOR = "vendor", "Vendor"

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED_AMOUNT = "fixed_amount", "Fixed amount"

    code = models.CharField(max_length=50, unique=True)
    scope = models.CharField(max_length=20, choices=Scope.choices)
    vendor_store = models.ForeignKey(
        VendorStore,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coupons",
    )
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_uses_total = models.PositiveIntegerField(null=True, blank=True)
    max_uses_per_user = models.PositiveIntegerField(null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class CouponRedemption(BaseModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="redemptions")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="coupon_redemptions")
    order = models.ForeignKey(
        "orders.Order", on_delete=models.PROTECT, related_name="coupon_redemptions"
    )
