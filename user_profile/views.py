from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from user_profile.models import UserProfile
from user_profile.permissions import IsOwnerOrReadOnly
from user_profile.serializers import ProfileSerializer


class UserProfileView(RetrieveUpdateAPIView):
    """
    API view for retrieving and partially updating a user's profile.

    Only the profile owner can perform updates; other users have read-only access.
    Full updates via PUT are disabled to enforce partial and safe updates only.

    URL Parameters:
        username (str): The username used to locate the corresponding UserProfile.

    Supported Methods:
        - GET: Retrieve the user's profile data.
        - PATCH: Partially update the user's profile if the requester is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Provides the queryset for the view.

        Returns:
            QuerySet: All UserProfile instances.
        """
        return UserProfile.objects.all()

    def get_object(self):
        """
        Retrieve the UserProfile object based on the username provided in the URL.

        Performs object-level permission checks to ensure that the requester has the correct access level.

        Returns:
            UserProfile: The profile instance associated with the given username.

        Raises:
            Http404: If no matching UserProfile is found.
        """
        username = self.kwargs.get('username')
        profile = get_object_or_404(UserProfile, user__username=username)

        # Enforce object-level permission
        self.check_object_permissions(self.request, profile)

        return profile

    def put(self, request, *args, **kwargs):
        """
        Disable full updates to user profiles.

        PUT is disallowed intentionally to avoid accidental data overwrites.
        """
        return Response(
            {'detail': 'PUT update not allowed. Use PATCH instead.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def patch(self, request, *args, **kwargs):
        """
        Partially update the user profile and nested user fields.

        Returns:
            - 200 OK with the updated profile data on success.
            - 400 Bad Request with validation errors on failure.
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteProfileView(DestroyAPIView):
    """
    API view to delete a user's profile and their associated user account.

    Only the profile owner is authorized to perform this action.

    URL Parameters:
        username (str): The username associated with the profile to delete.

    Supported Methods:
        - DELETE: Remove the UserProfile and the linked User instance.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Provides the queryset for the view.

        Returns:
            QuerySet: All UserProfile instances.
        """
        return UserProfile.objects.all()

    def get_object(self):
        """
        Retrieve the UserProfile object based on the username provided in the URL.

        Performs object-level permission checks to ensure the user has the correct access level.

        Returns:
            UserProfile: The profile instance associated with the given username.

        Raises:
            Http404: If no matching UserProfile is found.
        """
        username = self.kwargs.get('username')
        profile = get_object_or_404(UserProfile, user__username=username)

        # Enforce object-level permission
        self.check_object_permissions(self.request, profile)

        return profile

    def destroy(self, request, *args, **kwargs):
        """
        Delete the user's profile and associated user account.

        This method ensures a clean removal of both the profile and user data.

        Returns:
            Response: A 204 No Content response indicating successful deletion.
        """
        profile = self.get_object()
        user = profile.user

        # Delete the profile first
        profile.delete()

        # Then delete the associated user account
        user.delete()

        return Response(
            {'detail': 'Delete profile success'},
            status=status.HTTP_204_NO_CONTENT
        )
