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


class Permission(models.TextChoices):
    """Granular role-gated actions, codifying the Resource x Role matrix in
    docs/08-security-plan.md. Paired with ROLE_PERMISSIONS in
    apps/common/permissions.py.

    Only the actions where roles genuinely diverge in *capability* are
    listed here (e.g. admin can manage any store, a vendor only their own).
    Plain "own resource" read/write available to every authenticated role
    (own profile, own cart, own orders) is an ownership check, not a role
    grant, and stays out of this list — see each app's own permissions.py.
    """

    READ_ALL_ORDERS = "read_all_orders", "Read all customers' orders"
    MANAGE_OWN_STORE = "manage_own_store", "Manage own vendor store & products"
    MANAGE_ANY_STORE = "manage_any_store", "Manage any vendor's store & products"
    MANAGE_OWN_SUB_ORDERS = "manage_own_sub_orders", "Manage own vendor sub-orders"
    MANAGE_ANY_SUB_ORDERS = "manage_any_sub_orders", "Manage any vendor's sub-orders"
    READ_OWN_PAYOUTS = "read_own_payouts", "Read own payouts"
    MANAGE_ALL_PAYOUTS = "manage_all_payouts", "Full control over payouts"
    APPROVE_VENDOR = "approve_vendor", "Approve, reject, or suspend vendor applications"
    CREATE_VENDOR_COUPON = "create_vendor_coupon", "Create vendor-scoped coupons"
    CREATE_PLATFORM_COUPON = "create_platform_coupon", "Create platform-wide coupons"
    MANAGE_CATALOG_TAXONOMY = "manage_catalog_taxonomy", "Manage categories & brands"
    DECIDE_OWN_REFUNDS = "decide_own_refunds", "Decide refunds on own sub-orders"
    DECIDE_ANY_REFUND = "decide_any_refund", "Decide any refund"
