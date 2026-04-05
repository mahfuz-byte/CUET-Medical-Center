from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, MedicineViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'medicines', MedicineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
