"""accounts: custom User + Address models (docs/10-project-structure.md).

Django requires AUTH_USER_MODEL to point at a real model from the very
first migration, so a minimal swappable User is created here in Phase 0.
The `role` field and the rest of Phase 1.1 (auth flows, Address CRUD) land
as a follow-up migration, not a fresh model swap.
"""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
