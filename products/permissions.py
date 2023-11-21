from rest_framework import permissions
from rest_framework.request import HttpRequest

from users.models.user import User


class SuperUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return False
