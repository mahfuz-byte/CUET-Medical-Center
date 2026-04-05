from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BloodDonorViewSet, BloodRequestViewSet

router = DefaultRouter()
router.register(r'donors', BloodDonorViewSet, basename='donor')
router.register(r'requests', BloodRequestViewSet, basename='bloodrequest')

urlpatterns = [
    path('', include(router.urls)),
]
