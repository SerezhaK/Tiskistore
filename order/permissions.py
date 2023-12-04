from rest_framework import permissions
from rest_framework.request import HttpRequest

from users.models.user import User


class UserOwner(permissions.BasePermission):
    def has_permission(self,request: HttpRequest, view):
        if not request.user.is_authenticated:
            return False
        return True
    def has_object_permission(self, request: HttpRequest, view, obj: User):
        if not request.user.is_authenticated:
            return False
        if obj.user_id == request.user.user_id:
            return True
        if request.user.is_staff:
            return True
        return False
