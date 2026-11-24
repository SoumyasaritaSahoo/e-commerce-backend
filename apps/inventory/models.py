"""inventory: Inventory, InventoryLog (docs/05-database-design.md)."""

from django.db import models

from apps.catalog.models import ProductVariant
from apps.common.models import BaseModel


class Inventory(BaseModel):
    variant = models.OneToOneField(
        ProductVariant, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity_available__gte=0),
                name="inventory_quantity_available_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(quantity_reserved__gte=0),
                name="inventory_quantity_reserved_gte_0",
            ),
        ]

    def __str__(self):
        return f"{self.variant.sku}: {self.quantity_available} available"


class InventoryLog(BaseModel):
    class Reason(models.TextChoices):
        RESTOCK = "restock", "Restock"
        ORDER_PLACED = "order_placed", "Order placed"
        ORDER_CANCELLED = "order_cancelled", "Order cancelled"
        REFUND = "refund", "Refund"
        MANUAL_ADJUSTMENT = "manual_adjustment", "Manual adjustment"

    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="inventory_logs"
    )
    change_qty = models.IntegerField()
    reason = models.CharField(max_length=20, choices=Reason.choices)
    reference_id = models.CharField(max_length=100, null=True, blank=True)
