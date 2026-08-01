"""Enums shared across multiple apps.

Only put an enum here if the exact same set of values is genuinely reused
by more than one app. Status enums that belong to a single model (e.g.
Order.status, Payment.status, VendorStore.status — see
docs/05-database-design.md) stay local to that model's own app instead of
being forced into a shared class here, since their value sets don't
actually match one another despite superficially similar-looking tokens
(e.g. "pending", "approved").
"""

from django.db import models


class Role(models.TextChoices):
    """User.role — referenced for permission checks across nearly every
    app (vendors, catalog, orders, payments, ...), not just accounts."""

    CUSTOMER = "customer", "Customer"
    VENDOR = "vendor", "Vendor"
    ADMIN = "admin", "Admin"
