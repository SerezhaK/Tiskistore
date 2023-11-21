import random

from django.conf import settings
from rest_framework import mixins, viewsets

from users.serializers.users import (UserCreateCustomSerializer,
                                     UserListSerializer, UserUpdateSerializer)

import datetime
from ..mixins.user import UserMixin
from ..models.user import User
# from .. import UserOwnerOrReadOnly
# from ..serializers.users import
from ..services.phone_number import send_phone_number_verification
from phone_activation.models import Phone_date
from ..mixins.phone_number import PhoneNumberMixin


# from users.permissions.user import UserOwnerOrReadOnly


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,
                  UserMixin,
                  PhoneNumberMixin
                  ):
    queryset = User.objects.all()

    # permission_classes = [UserOwnerOrReadOnly]
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
        control_value = str(random.randint(100000, 999999))
        user = serializer.save(is_active=False)
        Phone_date.objects.create(user=user, control_code=control_value, activation_time=datetime.datetime.now())
        send_phone_number_verification(user=user, control_value=control_value, viewset_instance=self)
