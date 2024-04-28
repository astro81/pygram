from django.urls import path
from messaging.views import (
    ConversationListView,
    ConversationDetailView,
    MessageCreateView,
    UserSearchView
)

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<uuid:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<uuid:conversation_id>/messages/', MessageCreateView.as_view(), name='message-create'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
]