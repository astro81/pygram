from rest_framework import serializers
from messaging.models import Conversation, Message
from user_profile.serializers import ProfileSerializer

from django.contrib.auth import get_user_model
User = get_user_model()  # Add this at the top

class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'created_at', 'read']
        read_only_fields = ['id', 'sender', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message', 'unread_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(read=False).exclude(sender=request.user).count()
        return 0


class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Conversation
        fields = ['participant_ids']

    def validate_participant_ids(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required.")
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        current_user = self.context['request'].user

        # Get all participants including current user
        participants = User.objects.filter(id__in=participant_ids)
        participants = list(participants) + [current_user]

        # Check if conversation already exists with exactly these participants
        existing_conversation = None
        for conv in Conversation.objects.all():
            if set(conv.participants.all()) == set(participants):
                existing_conversation = conv
                break

        if existing_conversation:
            return existing_conversation

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation