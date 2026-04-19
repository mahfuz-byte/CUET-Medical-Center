from django.contrib import admin
from .models import Inventory, Medicine, MedicalRecord


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'quantity']
    list_filter = ['item_type']
    search_fields = ['name']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'dosage']
    search_fields = ['name']


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'doctor', 'diagnosis', 'created_at']
    list_filter = ['created_at']
    search_fields = ['student__email', 'student__student_id', 'diagnosis']
