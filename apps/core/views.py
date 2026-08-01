"""Shared, cross-app views. Currently just the health check
(docs/11-deployment-infra.md: "/healthz/ endpoint (checks DB + Redis
connectivity) wired to the load balancer and uptime monitoring")."""

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def healthz(request):
    checks = {"db": False, "redis": False}

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["db"] = True
    except Exception:
        pass

    try:
        cache.set("healthz", "ok", timeout=5)
        checks["redis"] = cache.get("healthz") == "ok"
    except Exception:
        pass

    healthy = all(checks.values())
    return JsonResponse(
        {"status": "ok" if healthy else "unhealthy", "checks": checks},
        status=200 if healthy else 503,
    )
