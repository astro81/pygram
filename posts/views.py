from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostSerializer
from posts.permissions import IsOwnerOrReadOnly


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                "message": "Post created successfully!",
                "data": response.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "message": "Failed to create post.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response({
                "message": "Post updated successfully.",
                "data": response.data
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "message": "Failed to update post.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        try:
            instance: object = self.get_object()
            self.perform_destroy(instance)
            return Response({
                "message": "Post deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({
                "message": "Failed to delete post.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)