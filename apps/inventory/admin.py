from django.contrib import admin

from .models import Inventory, InventoryLog


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["variant", "quantity_available", "quantity_reserved", "low_stock_threshold"]
    search_fields = ["variant__sku"]


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ["variant", "change_qty", "reason", "created_at"]
    list_filter = ["reason"]
    search_fields = ["variant__sku"]
