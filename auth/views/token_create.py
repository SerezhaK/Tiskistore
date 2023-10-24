from djoser import utils
from djoser.serializers import TokenCreateSerializer, UserCreateSerializer
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.response import Response

from ..serializers import CustomTokenSerializer


class CustomTokenCreateView(TokenCreateView):
    serializer_class = UserCreateSerializer

    def post(self, request, **kwargs):
        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer)

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        return Response(
            data=CustomTokenSerializer(token).data, status=status.HTTP_200_OK
        )
