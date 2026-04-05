from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'target', 'created_by', 'created_by_detail', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
