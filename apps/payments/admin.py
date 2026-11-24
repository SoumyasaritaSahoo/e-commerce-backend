from django.contrib import admin

from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["order", "gateway", "method", "amount", "status"]
    list_filter = ["status", "method", "gateway"]
    search_fields = ["order__order_number", "gateway_payment_id"]


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ["payment", "vendor_sub_order", "amount", "status", "requested_at"]
    list_filter = ["status"]
