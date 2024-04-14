from rest_framework import serializers
from user_profile.models import UserProfile
from django.contrib.auth import get_user_model

# Get the user model (custom or default)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Serializes basic user information including:
    - id
    - username
    - email
    - first_name
    - last_name
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Includes a nested UserSerializer to manage related user fields.
    Also performs validation to ensure the uniqueness of the username and email.
    """
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'profile_pic', 'bio']
        extra_kwargs = {'user': {'required': True}}

    def validate(self, attrs):
        """
        Validate nested user data to ensure that the username and email are unique.

        Args:
            attrs (dict): The attributes to be validated.

        Returns:
            dict: Validated attributes.

        Raises:
            serializers.ValidationError: If username or email is already taken.
        """
        user_data = attrs.get('user', {})
        user_instance = self.instance.user if self.instance else None

        # Check if the username is already in use
        username = user_data.get('username')
        if username:
            qs = User.objects.filter(username=username)
            if user_instance:
                qs = qs.exclude(pk=user_instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'username': 'This username is already taken.'})

        # Check if the email is already in use
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
        Update an existing UserProfile instance along with its related User data.

        Args:
            instance (UserProfile): The UserProfile instance to update.
            validated_data (dict): The validated data for update.

        Returns:
            UserProfile: The updated UserProfile instance.
        """
        # Extract nested user data
        user_data = validated_data.pop('user', None)

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related User fields if user data is provided
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        return instance
