from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    Includes a read-only username field derived from the related user,
    and handles the serialization of post data for API responses.

    Fields:
        - id (UUID): Unique identifier of the post.
        - username (str): Read-only field displaying the post owner's username.
        - caption (str): Optional caption text.
        - post_image (ImageField): Optional image file.
        - created_at (datetime): Timestamp when the post was created.
    """
    username = serializers.CharField(
        source='user.username',
        read_only=True,
        help_text="Username of the post creator"
    )

    class Meta:
        model = Post
        fields = ['id', 'username', 'caption', 'post_image', 'created_at']
        read_only_fields = ['user']

    def validate(self, data):
        # Get the caption and post_image from incoming data or instance (on update)
        caption = data.get('caption') if 'caption' in data else getattr(self.instance, 'caption', None)
        post_image = data.get('post_image') if 'post_image' in data else getattr(self.instance, 'post_image', None)

        if not caption and not post_image:
            # raise serializers.ValidationError("Either Caption or Post Image must be provided.")
            raise serializers.ValidationError(["Either Caption or Post Image must be provided."])

        return data

