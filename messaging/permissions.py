from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    """
    Check if the user is a participant of the conversation
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()