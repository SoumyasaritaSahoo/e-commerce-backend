from django.contrib import admin

from .models import Order, OrderItem, Shipment, VendorSubOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "status", "grand_total", "placed_at"]
    list_filter = ["status"]
    search_fields = ["order_number", "user__email"]
    inlines = [OrderItemInline]


@admin.register(VendorSubOrder)
class VendorSubOrderAdmin(admin.ModelAdmin):
    list_display = ["order", "vendor_store", "status", "payout_status", "subtotal"]
    list_filter = ["status", "payout_status"]
    search_fields = ["order__order_number", "vendor_store__store_name"]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["vendor_sub_order", "carrier", "tracking_number", "shipped_at", "delivered_at"]
