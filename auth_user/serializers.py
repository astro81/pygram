from rest_framework import serializers
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Includes password confirmation and ensures that the provided passwords match.
    Uses Django's `create_user` method to handle password hashing.
    """
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True,
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True}  # Ensure email is a required field
        }

    def validate(self, data):
        """
        Validates that the two entered passwords match.

        Raises:
            serializers.ValidationError: If passwords do not match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        """
        Creates a new user with the validated data.

        Returns:
            User: The created user instance.
        """
        validated_data.pop('password2')  # Remove password2 as it's not part of the User model
        user = User.objects.create_user(**validated_data)
        return user
