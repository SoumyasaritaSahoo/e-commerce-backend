from django.contrib import admin

from .models import Payout, PayoutItem


class PayoutItemInline(admin.TabularInline):
    model = PayoutItem
    extra = 0


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ["vendor_store", "period_start", "period_end", "total_amount", "status"]
    list_filter = ["status"]
    search_fields = ["vendor_store__store_name"]
    inlines = [PayoutItemInline]
