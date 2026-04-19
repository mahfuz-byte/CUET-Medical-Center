from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Notification, Notice
from .serializers import NotificationSerializer, NoticeSerializer


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


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        """Add request to serializer context for absolute URL building"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        """
        Allow anyone to view notices,
        but only admin and doctor can create/update/delete
        """
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            from rest_framework.permissions import IsAuthenticated
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        # Check if user is admin or doctor
        user = self.request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role not in ['admin', 'doctor']:
            return Response(
                {'detail': 'Only admin and doctor can publish notices.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(created_by=user)

    def create(self, request, *args, **kwargs):
        # Custom create to add role check
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role not in ['admin', 'doctor']:
            return Response(
                {'detail': 'Only admin and doctor can publish notices.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def list_notices(self, request):
        """List all notices (public endpoint)"""
        notices = self.get_queryset()
        serializer = self.get_serializer(notices, many=True)
        return Response(serializer.data)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsDoctorOrAdminWriteElseReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        """Add request to serializer context for absolute URL building"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        """
        Allow anyone to view notices,
        but only admin and doctor can create/update/delete
        """
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            from rest_framework.permissions import IsAuthenticated
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        # Check if user is admin or doctor
        user = self.request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role not in ['admin', 'doctor']:
            return Response(
                {'detail': 'Only admin and doctor can publish notices.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(created_by=user)

    def create(self, request, *args, **kwargs):
        # Custom create to add role check
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role not in ['admin', 'doctor']:
            return Response(
                {'detail': 'Only admin and doctor can publish notices.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def list_notices(self, request):
        """List all notices (public endpoint)"""
        notices = self.get_queryset()
        serializer = self.get_serializer(notices, many=True)
        return Response(serializer.data)
