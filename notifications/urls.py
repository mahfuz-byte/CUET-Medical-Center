from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NoticeViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'notices', NoticeViewSet, basename='notice')

urlpatterns = [
    path('', include(router.urls)),
]
