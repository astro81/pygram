from django.urls import path

from user_profile.views import UserProfileView, UserDeleteProfileView

urlpatterns = [
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/delete/', UserDeleteProfileView.as_view(), name='delete-profile'),
]

