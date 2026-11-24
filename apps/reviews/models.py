"""reviews: Review (docs/05-database-design.md).

Adds `is_active` — the doc's cross-cutting soft-delete rule requires it
for Review, but the model's own field list in the doc omits it.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.accounts.models import User
from apps.catalog.models import Product
from apps.common.models import BaseModel
from apps.orders.models import OrderItem


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reviews")
    order_item = models.OneToOneField(
        OrderItem, on_delete=models.CASCADE, related_name="review"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_review_user_product")
        ]
