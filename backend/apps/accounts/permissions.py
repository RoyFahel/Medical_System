from rest_framework.permissions import BasePermission
from .models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN)
from rest_framework.permissions import BasePermission


class IsAdminHeader(BasePermission):
    def has_permission(self, request, view):
        return request.headers.get("X-User-Role") == "admin"