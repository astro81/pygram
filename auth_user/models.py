import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.

    This model replaces the default integer-based ID with a UUID for better
    uniqueness and security. All other fields and behavior are inherited from AbstractUser.
    """

    # Use a UUID as the primary key instead of the default auto-incrementing ID.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """
        Returns a string representation of the user instance.
        """
        return self.username
