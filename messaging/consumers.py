import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from messaging.models import Conversation, Message
from user_profile.models import UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'

        # Check if user is authenticated and part of the conversation
        user = self.scope['user']
        if user == AnonymousUser():
            await self.close()
            return

        if not await self.is_participant(user):
            await self.close()
            return

        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def is_participant(self, user):
        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=user
        ).exists()

    @database_sync_to_async
    def create_message(self, sender, message):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=message
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Save message to database
        message_obj = await self.create_message(user, message)

        # Send message to conversation group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
                'timestamp': str(message_obj.created_at)
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))