import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Get the custom User model
User = get_user_model()

class UserProfile(models.Model):
    """
    Model to store additional user profile information.

    Fields:
        - id (UUID): Primary key, auto-generated UUID for uniqueness.
        - user (OneToOne): One-to-one link to the User model.
        - profile_pic (ImageField): Optional profile image uploaded by the user.
        - bio (TextField): Optional short biography or user description.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="Link to the user this profile belongs to"
    )
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        help_text="Optional profile picture"
    )
    bio = models.TextField(
        null=True,
        blank=True,
        help_text="Optional bio or user description"
    )

    def __str__(self):
        """
        String representation of the UserProfile.

        Returns:
            str: Username of the associated user.
        """
        return self.user.username
