from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """Allow access only to students."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsDoctor(BasePermission):
    """Allow access only to doctors."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'


class IsAdmin(BasePermission):
    """Allow access only to admins."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsDoctorOrAdmin(BasePermission):
    """Allow access to doctors or admins."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['doctor', 'admin']
