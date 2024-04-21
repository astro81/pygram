from rest_framework import serializers
from user_profile.models import UserProfile
from django.contrib.auth import get_user_model

# Get the user model (custom or default)
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model with flattened user fields.

    Exposes the related User model's fields (username, email, etc.) directly in the output.
    Also performs validation to ensure the uniqueness of username and email.
    """
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_pic',
            'bio'
        ]

    def validate(self, attrs):
        """
        Validate nested user data to ensure uniqueness of username and email.

        Args:
            attrs (dict): The attributes to validate.

        Returns:
            dict: Validated attributes.

        Raises:
            serializers.ValidationError: If username or email already exists.
        """
        user_data = attrs.get('user', {})
        user_instance = self.instance.user if self.instance else None

        username = user_data.get('username')
        if username:
            qs = User.objects.filter(username=username)
            if user_instance:
                qs = qs.exclude(pk=user_instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'username': 'This username is already taken.'})

        email = user_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if user_instance:
                qs = qs.exclude(pk=user_instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'email': 'This email is already taken.'})

        return attrs

    def update(self, instance, validated_data):
        """
        Update an existing UserProfile instance along with nested User data.

        Args:
            instance (UserProfile): The instance to update.
            validated_data (dict): Validated data.

        Returns:
            UserProfile: Updated profile instance.
        """
        user_data = validated_data.pop('user', {})

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested User fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance
