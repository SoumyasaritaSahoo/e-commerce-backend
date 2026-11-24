"""Role-based DRF permission primitives, reused across every app.

docs/08-security-plan.md requires role enforcement via "DRF permission
classes on every view — never inferred client-side," and confirms
`role == "admin"` (not Django's is_staff/is_superuser) is the sole
authorization source for the "admin" role.

Per-app *ownership* permission classes (e.g. "is this vendor's own
product") deliberately do NOT live here — they belong in each app's own
permissions.py, built alongside that app's views, not speculatively now.
"""

from rest_framework.permissions import BasePermission

from apps.common.choices import Permission, Role

ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.CUSTOMER: frozenset(),
    Role.VENDOR: frozenset(
        {
            Permission.MANAGE_OWN_STORE,
            Permission.MANAGE_OWN_SUB_ORDERS,
            Permission.READ_OWN_PAYOUTS,
            Permission.CREATE_VENDOR_COUPON,
            Permission.DECIDE_OWN_REFUNDS,
        }
    ),
    Role.ADMIN: frozenset(
        {
            Permission.READ_ALL_ORDERS,
            Permission.MANAGE_ANY_STORE,
            Permission.MANAGE_ANY_SUB_ORDERS,
            Permission.MANAGE_ALL_PAYOUTS,
            Permission.APPROVE_VENDOR,
            Permission.CREATE_PLATFORM_COUPON,
            Permission.MANAGE_CATALOG_TAXONOMY,
            Permission.DECIDE_ANY_REFUND,
        }
    ),
}


def permission_required(permission: Permission):
    """DRF permission class factory keyed off ROLE_PERMISSIONS.

    Usage: `permission_classes = [permission_required(Permission.APPROVE_VENDOR)]`
    """

    class _HasPermission(BasePermission):
        def has_permission(self, request, view):
            if not (request.user and request.user.is_authenticated):
                return False
            return permission in ROLE_PERMISSIONS.get(request.user.role, frozenset())

    return _HasPermission


class IsCustomerRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == Role.CUSTOMER
        )


class IsVendorRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == Role.VENDOR
        )


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == Role.ADMIN
        )


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_email_verified
        )
