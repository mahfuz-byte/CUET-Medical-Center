from django.contrib import admin
from .models import Inventory, Medicine


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'quantity']
    list_filter = ['item_type']
    search_fields = ['name']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'dosage']
    search_fields = ['name']
