from django.contrib import admin

from .models import Coupon, CouponRedemption


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "scope", "discount_type", "discount_value", "is_active", "valid_until"]
    list_filter = ["scope", "discount_type", "is_active"]
    search_fields = ["code"]


@admin.register(CouponRedemption)
class CouponRedemptionAdmin(admin.ModelAdmin):
    list_display = ["coupon", "user", "order", "created_at"]
    search_fields = ["coupon__code", "user__email", "order__order_number"]
