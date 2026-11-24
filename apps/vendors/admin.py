from django.contrib import admin

from .models import VendorStore


@admin.register(VendorStore)
class VendorStoreAdmin(admin.ModelAdmin):
    list_display = ["store_name", "owner_user", "status", "commission_rate", "created_at"]
    list_filter = ["status"]
    search_fields = ["store_name", "owner_user__email"]
