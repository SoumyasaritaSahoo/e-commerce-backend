"""cart: Cart, CartItem, WishlistItem (docs/05-database-design.md)."""

from django.db import models

from apps.accounts.models import User
from apps.catalog.models import ProductVariant
from apps.common.models import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="carts"
    )
    session_key = models.CharField(max_length=100, null=True, blank=True)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="+")
    quantity = models.PositiveIntegerField(default=1)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cart", "variant"], name="unique_cart_variant")
        ]


class WishlistItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="+")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "variant"], name="unique_wishlist_user_variant")
        ]
