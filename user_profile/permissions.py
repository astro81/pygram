from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only the owner of an object to edit it.

    - Read permissions are allowed to any request (GET, HEAD, OPTIONS).
    - Write permissions are only allowed to the owner of the object.

    Usage:
        Attach this permission class to views where you want to ensure that
        only the owner of a resource can modify it, but everyone can read it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for safe methods (e.g., GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow write permissions to the owner of the object
        return request.user.is_authenticated and obj.user == request.user
