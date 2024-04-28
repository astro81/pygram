from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404

from messaging.models import Conversation, Message
from messaging.serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)
from user_profile.serializers import ProfileSerializer


class ConversationListView(generics.ListCreateAPIView):
    """
    List all conversations for the current user or create a new conversation
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related('participants', 'messages')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        # Return the full conversation details
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConversationDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single conversation with all its messages
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def get_object(self):
        conversation = super().get_object()

        # Mark all unread messages as read
        Message.objects.filter(
            conversation=conversation,
            read=False
        ).exclude(
            sender=self.request.user
        ).update(read=True)

        return conversation


class MessageCreateView(generics.CreateAPIView):
    """
    Create a new message in a conversation
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=request.user),
            id=conversation_id
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)

        # Update conversation's updated_at
        conversation.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSearchView(generics.ListAPIView):
    """
    Search users by username for starting new conversations
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        from user_profile.models import UserProfile
        query = self.request.query_params.get('q', '')
        return UserProfile.objects.filter(
            user__username__icontains=query
        ).exclude(
            user=self.request.user
        )