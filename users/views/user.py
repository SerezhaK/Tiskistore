from django.conf import settings
from rest_framework import mixins, viewsets

from users.serializers.users import (UserCreateCustomSerializer,
                                     UserListSerializer, UserUpdateSerializer)
from ..mixins.phone_number import PhoneNumberMixin
from ..mixins.user import UserMixin
from ..models.user import User
from ..permissions import UserOwnerOrReadOnly
from ..services.phone_number import send_phone_number_verification


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,
                  UserMixin,
                  PhoneNumberMixin
                  ):
    queryset = User.objects.all()

    permission_classes = [UserOwnerOrReadOnly]
    serializer_class = UserCreateCustomSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateCustomSerializer
        if self.action in ('update', 'partial_update'):
            return UserUpdateSerializer
        return UserListSerializer

    def perform_create(self, serializer: UserCreateCustomSerializer):
        if not settings.PHONE_NUMBER_CONFIRM:
            serializer.save(is_active=True)
            return
        user = serializer.save(is_active=False)
        send_phone_number_verification(
            user=user,
            viewset_instance=self
        )
