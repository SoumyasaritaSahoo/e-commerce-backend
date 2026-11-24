"""orders: Order, VendorSubOrder, OrderItem, Shipment
(docs/05-database-design.md).

Order.coupon uses a string reference ("promotions.Coupon") since
promotions.Coupon.vendor_store / CouponRedemption.order create a circular
app dependency between orders and promotions.
"""

from django.db import models

from apps.accounts.models import Address, User
from apps.catalog.models import ProductVariant
from apps.common.models import BaseModel
from apps.vendors.models import VendorStore


class Order(BaseModel):
    class Status(models.TextChoices):
        PENDING_PAYMENT = "pending_payment", "Pending payment"
        PAID = "paid", "Paid"
        PARTIALLY_FULFILLED = "partially_fulfilled", "Partially fulfilled"
        FULFILLED = "fulfilled", "Fulfilled"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    order_number = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    shipping_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="shipping_orders"
    )
    billing_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="billing_orders"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(
        "promotions.Coupon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    placed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "-placed_at"])]

    def __str__(self):
        return self.order_number


class VendorSubOrder(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PACKED = "packed", "Packed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        RETURNED = "returned", "Returned"

    class PayoutStatus(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        INCLUDED_IN_PAYOUT = "included_in_payout", "Included in payout"
        PAID = "paid", "Paid"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="sub_orders")
    vendor_store = models.ForeignKey(
        VendorStore, on_delete=models.PROTECT, related_name="sub_orders"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout_status = models.CharField(
        max_length=20, choices=PayoutStatus.choices, default=PayoutStatus.UNPAID
    )

    class Meta:
        indexes = [models.Index(fields=["vendor_store", "status"])]


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    vendor_sub_order = models.ForeignKey(
        VendorSubOrder, on_delete=models.CASCADE, related_name="items"
    )
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="+")
    product_title_snapshot = models.CharField(max_length=255)
    unit_price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)


class Shipment(BaseModel):
    vendor_sub_order = models.ForeignKey(
        VendorSubOrder, on_delete=models.CASCADE, related_name="shipments"
    )
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
