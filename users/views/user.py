from django.conf import settings
from rest_framework import mixins, viewsets

from users.serializers.users import (UserCreateCustomSerializer,
                                     UserListSerializer, UserUpdateSerializer)

from ..mixins.email import EmailMixin
from ..mixins.user import UserMixin
from ..models.user import User
from ..permissions import UserOwnerOrReadOnly
# from ..serializers.users import
from ..services import send_email_verification

# from users.permissions.user import UserOwnerOrReadOnly


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,
                  UserMixin,
                  EmailMixin
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
        if not settings.EMAIL_CONFIRM:
            serializer.save(is_active=True)
            return
        user = serializer.save(is_active=False)
        send_email_verification(user=user, viewset_instance=self)
