from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message
from notifications.models import Notification  # Assuming you have a notifications app


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        sender = instance.sender

        for participant in conversation.participants.all():
            if participant != sender:
                Notification.objects.create(
                    recipient=participant,
                    actor=sender,
                    verb='sent you a message',
                    target=conversation,
                    description=instance.text[:50]  # First 50 chars of message
                )