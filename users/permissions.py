from rest_framework import permissions
from rest_framework.request import HttpRequest

from users.models.user import User


class UserOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view, obj=None):
        if request.method == "POST":
            return True
        if not request.user.is_authenticated:
            return False
        if obj is not None:
            return True
        return request.user.is_staff

    def has_object_permission(self, request: HttpRequest, view, obj: User):
        if request.method == "POST":
            return True
        if not request.user.is_authenticated:
            return False
        return obj.user_id == request.user.user_id or request.user.is_staff
