"""api/v1 root — includes each app's urls.py under /api/v1/<app>/
(docs/06-api-design.md, Phase 0 of docs/14-execution-checklist.md).

Every app is wired here even before it has real endpoints so the app
skeletons are provably reachable from Phase 0 onward.
"""

from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.accounts.urls")),
    path("vendors/", include("apps.vendors.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("cart/", include("apps.cart.urls")),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("payouts/", include("apps.payouts.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("promotions/", include("apps.promotions.urls")),
    path("notifications/", include("apps.notifications.urls")),
]
