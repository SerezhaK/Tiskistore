from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.user import User
from ..services.phone_number import (get_new_password_from_cache,
                                     get_redis_key_from_cache,
                                     send_phone_number_verification)


def get_user_for_confirm(
        user_id: int = None,
        phone_number: str = None
):
    if user_id:
        return get_object_or_404(User, user_id=user_id)

    try:
        phone_number_valid = PhoneNumber.from_string(
            phone_number=phone_number,
            region='RU'
        ).as_e164
    except BaseException:
        return Response(
            'Код не верный #p',
            status=status.HTTP_200_OK,
        )
    return get_object_or_404(User, phone_number=phone_number_valid)


class PhoneNumberMixin:

    @action(
        methods=['POST'],
        url_path='confirm_active_user',
        detail=False,
        url_name='confirm_active_user',
    )
    def confirm_active_user(self, request):
        if "phone_number" not in request.data:
            return Response(
                'Код не верный, попробуйте еще раз #ph',
                status=status.HTTP_200_OK,
            )
        if "redis_key" not in request.data:
            return Response(
                'Код не верный, попробуйте еще раз #re',
                status=status.HTTP_200_OK,
            )

        user = get_user_for_confirm(
            phone_number=request.data["phone_number"]
        )

        if not settings.PHONE_NUMBER_CONFIRM:
            user.is_active = True
            user.save()
            return Response(
                'Успешно!',
                status=status.HTTP_200_OK,
            )

        if get_redis_key_from_cache(user) == request.data["redis_key"]:
            user.is_active = True
            user.save()
            return Response(
                'Успешно!',
                status=status.HTTP_200_OK,
            )

        return Response(
            'Код неверный, попробуйте еще раз',
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        url_path='resent_confirm_active_user',
        detail=False,
        url_name='resent_confirm_active_user',
    )
    def resent_confirm_active_user(self, request):
        if "phone_number" not in request.data:
            return Response(
                'Код не верный, попробуйте еще раз #pр',
                status=status.HTTP_200_OK,
            )

        user = get_user_for_confirm(
            phone_number=request.data["phone_number"]
        )

        if not settings.PHONE_NUMBER_CONFIRM:
            return Response(
                "Код подтверждения отправлен на номер телефона:"
                f" {request.data['phone_number']}",
                status=status.HTTP_200_OK,
            )

        send_phone_number_verification(
            user=user,
            viewset_instance=self
        )

        return Response(
            "Код подтверждения отправлен на номер телефона:"
            f" {request.data['phone_number']}",
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        url_path='change_password',
        detail=False,
        url_name='change_password',
    )
    def change_password(self, request):
        if "phone_number" not in request.data:
            return Response(
                'Код не верный, попробуйте еще раз #ph',
                status=status.HTTP_200_OK,
            )
        if "new_password" not in request.data:
            return Response(
                'Код не верный, попробуйте еще раз #np',
                status=status.HTTP_200_OK,
            )

        user = get_user_for_confirm(
            phone_number=request.data["phone_number"]
        )
        new_password = request.data['new_password']

        try:
            validate_password(new_password)
        except BaseException:
            return Response(
                "Ненадежный пароль, попробуйте еще раз",
                status=status.HTTP_200_OK
            )

        if not settings.PHONE_NUMBER_CONFIRM:
            user.set_password(new_password)
            user.save()

        resp = send_phone_number_verification(
            user=user,
            new_password=new_password,
            viewset_instance=self
        )
        return Response(
            {resp},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        url_path='confirm_change_password',
        detail=False,
        url_name='confirm_change_password',
    )
    def confirm_change_password(self, request):
        if "phone_number" not in request.data:
            return Response(
                'Код не верный, попробуйте еще раз #ph',
                status=status.HTTP_200_OK,
            )
        if "redis_key" not in request.data:
            return Response(
                'Код не верный #re',
                status=status.HTTP_200_OK,
            )

        user = get_user_for_confirm(
            phone_number=request.data["phone_number"]
        )
        control_key = request.data["redis_key"]
        if get_redis_key_from_cache(user) == control_key:
            new_password = get_new_password_from_cache(
                user=user
            )
            user.set_password(new_password)
            user.save()
            return Response(
                'Пароль изменен успешно!',
                status=status.HTTP_200_OK
            )

        return Response(
            'Код не верный, попробуйте еще раз',
            status=status.HTTP_200_OK,
        )
