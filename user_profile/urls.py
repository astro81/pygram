from django.urls import path

from user_profile.views import UserProfileView

urlpatterns = [
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
]

