from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, AmbulanceViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'ambulances', AmbulanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
