import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Get the custom User model
User = get_user_model()

class Post(models.Model):
    """
    Model to store user-generated posts.

    Fields:
        - id (UUID): Primary key, auto-generated UUID for uniqueness.
        - user (ForeignKey): Reference to the user who created the post.
        - caption (TextField): Optional text caption describing the post.
        - post_image (ImageField): Optional image uploaded with the post.
        - created_at (DateTime): Timestamp when the post was created.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="Creator the post"
    )
    caption = models.TextField(
        blank=True,
        null=True,
        help_text="Optional caption for the post"
    )
    post_image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        help_text="Optional image for the post"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of post creation"
    )

    def __str__(self):
        """
        String representation of the Post.

        Returns:
            str: Username and truncated caption (first 40 characters).
        """
        return f'{self.user.username}: {self.caption[:40] if self.caption else ""}'

