from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet

router = DefaultRouter()
router.register('', PostViewSet, basename='posts')

urlpatterns = router.urls
