from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'caption', 'post_image', 'created_at']

        read_only_fields = ['user']

