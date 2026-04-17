from rest_framework import serializers
from .models import ChatHistory


class ChatMessageSerializer(serializers.Serializer):
    """Serialize chat messages"""
    message = serializers.CharField(max_length=2000)


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'user_message', 'ai_response', 'created_at']
        read_only_fields = ['id', 'created_at']
