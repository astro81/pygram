from django.contrib.auth import authenticate
from django.db import DatabaseError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_user.serializers import UserRegistrationSerializer

def handle_exception(error, message="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    """Utility function to generate a consistent error response."""
    return Response(
        {"message": message, "errors": str(error)},
        status=status_code,
    )

class UserRegistrationView(APIView):
    """
    API view to handle user registration.

    Allows unauthenticated users to create a new user account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to register a new user.

        Returns:
            - 201 Created: If registration is successful.
            - 400 Bad Request: If validation fails.
            - 500 Internal Server Error: On unexpected errors.
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            # Check if input data is valid
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'message': 'User registered successfully'},
                    status=status.HTTP_201_CREATED
                )

            # Return validation errors if any
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            return Response(
                {'message': 'Validation error', 'errors': str(ve)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DatabaseError as db:
            return Response(
                {'message': 'Database error', 'errors': str(db)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return handle_exception(e)


class UserLoginView(APIView):
    """
    API view to handle user login.

    Authenticates user credentials and returns an authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to authenticate a user.

        Returns:
            - 200 OK: If login is successful and a token is issued.
            - 400 Bad Request: If credentials are invalid or missing.
            - 500 Internal Server Error: On unexpected errors.
        """
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            # Ensure both fields are provided
            if not username or not password:
                return Response(
                    {'message': 'Login Failed!', 'errors': 'Username and password are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Authenticate user using Django's built-in authentication
            user = authenticate(username=username, password=password)

            if user:
                # Generate or retrieve the auth token
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

            return Response({'message': 'Login Failed!', 'errors': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return handle_exception(e)


class UserLogoutView(APIView):
    """
    API view to handle user logout.

    Requires user to be authenticated and deletes their auth token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to log out the user.

        Returns:
            - 200 OK: If logout is successful.
            - 404 Not Found: If auth token doesn't exist.
            - 500 Internal Server Error: On unexpected errors.
        """
        try:
            # Delete the user's authentication token to log them out
            request.user.auth_token.delete()
            return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)

        except (AttributeError, Token.DoesNotExist):
            return Response(
                {'message': 'Logout Failed!', 'errors': 'Token not found or already deleted'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return handle_exception(e)
