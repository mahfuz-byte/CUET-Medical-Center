from django.contrib import admin
from .models import Doctor, Ambulance


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'dept', 'hours']
    search_fields = ['name', 'dept', 'title']
    list_filter = ['dept']


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ['ambulance_id', 'status', 'contact']
    list_filter = ['status']
    search_fields = ['ambulance_id', 'contact']
