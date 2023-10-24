
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models.user import User

# from ..permissions.user import UserOwnerOrReadOnly
# from ..serializers.author import AuthorSerializer


class UserMixin:
    @extend_schema(tags=['profile'])
    @action(
        methods=['GET'],
        url_path='profile',
        detail=False,
        # permission_classes=[UserOwnerOrReadOnly, IsAuthenticated, ],
    )
    def profile(self, request: Request):
        return Response(self.get_serializer(request.user).data)

    @extend_schema(tags=['profile'])
    @profile.mapping.patch1
    def profile_update(self, request: Request):
        serializer = self.get_serializer(
            instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, validated_data=request.data)
        return Response(serializer.data)

    @extend_schema(tags=['profile'])
    @profile.mapping.delete
    def profile_delete(self, request: Request):
        user: User = request.user
        user.delete()
        return Response({'detail': 'Success'}, status=204)
