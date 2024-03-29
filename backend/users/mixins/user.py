from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest, Request
from rest_framework.response import Response

from ..models.user import User
from ..permissions import IsStuff
from ..serializers.users import UserCreateCustomSerializer


class UserMixin:
    @extend_schema(tags=['profile'])
    @action(
        methods=['GET'],
        url_path='profile',
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def profile(self, request: Request):
        return Response(
            self.get_serializer(request.user).data,
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['profile'])
    @profile.mapping.patch
    def profile_update(self, request: Request):
        serializer = self.get_serializer(
            instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, validated_data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['profile'])
    @extend_schema(tags=['profile'])
    @profile.mapping.delete
    def profile_delete(self, request: Request):
        user: User = request.user
        user.delete()
        return Response(
            {'detail': 'Success'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['POST'],
        url_path='admin_create',
        detail=False,
        permission_classes=[IsStuff],
    )
    def admin_create(self, request: HttpRequest):
        serializer = UserCreateCustomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(
                request.data,
                is_admin=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        methods=['POST'],
        url_path='by_admin_user_change',
        detail=True,
        permission_classes=[IsStuff],
    )
    def by_admin_user_change(self, request: HttpRequest, pk: int):
        serializer = UserCreateCustomSerializer()
        user = User.objects.filter(pk=pk).first()
        serializer.update(
            user,
            request.data,
        )
        return Response("Успешно!", status=status.HTTP_200_OK)
