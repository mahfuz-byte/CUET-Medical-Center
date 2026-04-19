from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, MedicineViewSet, MedicalRecordViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-records')

urlpatterns = [
    path('', include(router.urls)),
]
