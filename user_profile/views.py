from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_profile.models import UserProfile
from user_profile.serializers import ProfileSerializer


# Create your views here.
class UserProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(UserProfile, user__username=username)

