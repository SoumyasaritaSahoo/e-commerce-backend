"""
URL configuration for config project.

Every app's URLs are namespaced under /api/v1/... (docs/06-api-design.md),
so bumping the API version later means adding a parallel /api/v2/ include
here rather than touching each app.
"""

from django.contrib import admin
from django.urls import include, path

from apps.core.views import healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("api/v1/", include("config.api_v1_urls")),
]
