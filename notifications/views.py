from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Notification
from .serializers import NotificationSerializer


class IsDoctorOrAdminWriteElseReadOnly(BasePermission):
    """Allow read access to everyone, but only doctor/admin can create/update/delete alerts."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ['doctor', 'admin']


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsDoctorOrAdminWriteElseReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
