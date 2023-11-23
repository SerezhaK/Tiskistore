

from django.conf import settings
from django.shortcuts import get_object_or_404
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.user import User
from ..services.phone_number import (get_new_password_from_cache,
                                     get_redis_key_from_cache,
                                     send_phone_number_verification)


class PhoneNumberMixin:
    def get_user_for_confirm(
            self,
            user_id: int = None,
            phone_number: str = None
    ):
        if user_id:
            return get_object_or_404(User, user_id=user_id)
        return get_object_or_404(User, phone_number=phone_number)

    @action(
        methods=['POST'],
        url_path='confirm_active_user',
        detail=False,
        url_name='confirm_active_user',
    )
    def confirm_active_user(self, request):
        user_phone_number_no_valid = request.data["phone_number"]
        user_phone_number_valid = PhoneNumber.from_string(
            phone_number=user_phone_number_no_valid,
            region='RU'
        ).as_e164
        user = User.objects.get(phone_number=user_phone_number_valid)
        if get_redis_key_from_cache(user) == request.data["redis_key"]:
            user.is_active = True
            user.save()
            return Response(
                'Успешно!',
                status=status.HTTP_200_OK,
            )
        return Response(
            'Код не верный, попробуйте еще раз',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['POST'],
        url_path='confirm_change_password',
        detail=False,
        url_name='confirm_change_password',
    )
    def confirm_change_password(self, request):
        user: User = request.user
        control_key = request.data["redis_key"]
        if get_redis_key_from_cache(user) == control_key:
            new_password = get_new_password_from_cache(
                user=user
            )
            user.set_password(new_password)
            user.save()
            return Response(
                'Password changed',
                status=status.HTTP_200_OK
            )
        return Response(
            'Код не верный, попробуйте еще раз',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['POST'],
        url_path='change_password',
        detail=False,
        url_name='change_password',
    )
    def change_password(self, request):
        user: User = request.user
        new_password = request.data['new_password']

        if not settings.PHONE_NUMBER_CONFIRM:
            user.set_password(new_password)
            user.save()

        resp = send_phone_number_verification(
            user=user,
            new_password=new_password,
            viewset_instance=self
        )
        return Response(
            f'Data {resp}',
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        url_path='resent_confirm_active_user',
        detail=False,
        url_name='resent_confirm_active_user',
    )
    def resent_confirm_active_user(self, request):
        user_phone_number_no_valid = request.data["phone_number"]
        user_phone_number_valid = PhoneNumber.from_string(
            phone_number=user_phone_number_no_valid,
            region='RU'
        ).as_e164
        user = User.objects.get(phone_number=user_phone_number_valid)
        send_phone_number_verification(user=user,
                                       viewset_instance=self)
        return Response(
            f"Отправлен код на номер телефона: {user_phone_number_valid} ",
            status=status.HTTP_200_OK,
        )
