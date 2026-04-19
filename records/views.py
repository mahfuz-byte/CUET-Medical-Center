from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Inventory, Medicine, MedicalRecord
from .serializers import InventorySerializer, MedicineSerializer, MedicalRecordSerializer


class IsAdminWriteElseReadOnly(BasePermission):
    """Allow authenticated users to read, but only admins can modify records."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'admin'


class IsMedicalRecordAccess(BasePermission):
    """Doctor/Admin can write; students can only read their own records."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role in ['doctor', 'admin']

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['doctor', 'admin']:
            return True
        return request.method in SAFE_METHODS and obj.student_id == request.user.id

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAdminWriteElseReadOnly]

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminWriteElseReadOnly]


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related('student', 'doctor').all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsMedicalRecordAccess]

    def get_queryset(self):
        user = self.request.user
        base_qs = MedicalRecord.objects.select_related('student', 'doctor').all()

        if user.role == 'student':
            return base_qs.filter(student=user)

        student_id = self.request.query_params.get('student_id')
        if student_id and user.role in ['doctor', 'admin']:
            return base_qs.filter(student__student_id=student_id)

        return base_qs

