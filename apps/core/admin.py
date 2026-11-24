from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["action", "target_type", "target_id", "actor_id", "created_at"]
    list_filter = ["action", "target_type"]
    search_fields = ["target_type", "target_id"]
