from rest_framework import permissions
from rest_framework.request import HttpRequest


class SuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(
            self, request: HttpRequest, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
