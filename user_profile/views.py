from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView
from rest_framework.response import Response

from user_profile.models import UserProfile
from user_profile.permissions import IsOwnerOrReadOnly
from user_profile.serializers import ProfileSerializer

class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()

    def get_object(self):
        username = self.kwargs.get('username')
        profile = get_object_or_404(UserProfile, user__username=username)

        self.check_object_permissions(self.request, profile)

        return profile

    def put(self, request, *args, **kwargs):
        return Response({'detail': 'Put update not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

