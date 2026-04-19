from rest_framework import serializers
from .models import Notification, Notice
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'target', 'created_by', 'created_by_detail', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']


class NoticeSerializer(serializers.ModelSerializer):
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    pdf_file = serializers.SerializerMethodField()
    
    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'pdf_file', 'created_by', 'created_by_detail', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_pdf_file(self, obj):
        """Return absolute URL for PDF file"""
        if not obj.pdf_file:
            return None
        
        # Try to get the absolute URL if request is available
        request = self.context.get('request')
        if request:
            try:
                return request.build_absolute_uri(obj.pdf_file.url)
            except Exception:
                # Fallback if build_absolute_uri fails
                pass
        
        # Fallback to relative URL
        return obj.pdf_file.url
