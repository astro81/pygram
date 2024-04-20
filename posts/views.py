from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Post
from posts.serializers import PostSerializer
from posts.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user posts.

    Allows users to create, retrieve, update, and delete posts.
    Permissions:
        - Authenticated users can create posts.
        - Only post owners can update or delete their posts.
        - Unauthenticated users have read-only access.

    Supported Actions:
        - GET (list): Retrieve a list of all posts.
        - GET (retrieve): Retrieve a specific post by its ID.
        - POST (create): Create a new post (authenticated users only).
        - PUT/PATCH (update): Update an existing post (owners only).
        - DELETE (destroy): Delete a post (owners only).
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        """
        Retrieve a Post instance by its ID.

        Raises:
            NotFound: If no Post with the given ID exists.

        Returns:
            Post: The retrieved post instance.
        """
        try:
            return super().get_object()
        except NotFound:
            raise NotFound(detail="Post not found with given identifier.")

    def perform_create(self, serializer):
        """
        Save a new Post instance with the current authenticated user as the owner.

        Args:
            serializer (PostSerializer): Serializer containing validated post data.
        """
        serializer.save(user=self.request.user)

