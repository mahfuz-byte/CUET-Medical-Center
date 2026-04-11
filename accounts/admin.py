from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'student_id']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'password_plaintext')}),
        ('Personal Info', {'fields': ('first_name', 'phone', 'student_id')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'role', 'student_id', 'phone'),
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'otp_code', 'created_at', 'expires_at', 'is_used']
    list_filter = ['role', 'is_used', 'created_at']
    search_fields = ['email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'otp_code']
