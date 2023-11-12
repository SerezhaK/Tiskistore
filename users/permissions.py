from rest_framework import permissions
from rest_framework.request import HttpRequest

from users.models.user import User


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return False


class UserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if obj.user_id == request.user.user_id:
            return True
        if request.user.is_superuser:
            return True
        return False
