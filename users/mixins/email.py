from django.conf import settings
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from ..models.user import User
from ..services import (get_user_id_from_cache, send_email_reset_password,
                        send_email_verification)


class EmailMixin:
    def get_user_for_confirm(self, user_id: int = None, email: str = None):
        if user_id:
            return get_object_or_404(User, user_id=user_id)
        return get_object_or_404(User, email=email)

    @extend_schema(tags=['email'])
    @action(
        methods=['GET', ],
        url_path='confirm',
        detail=False,
        url_name='confirm',
    )
    def confirm(self, request: Request):
        user_id = get_user_id_from_cache(
            request.query_params.get('confirm_token', ''),
            prefix_key=settings.IT_BEL_USER_CONFIRM_KEY
        )
        if not user_id:
            return Response(
                'Token is invalid or expired. Please request/'
                ' another confirm email by signing in.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user: User = self.get_user_for_confirm(user_id=user_id)
        user.is_active = True
        user.save()

        return Response(
            status=status.HTTP_302_FOUND,
            headers={'Location': 'http://localhost:3000/signin'}
        )

    @extend_schema(tags=['email'])
    @action(
        methods=['POST', ],
        url_path='resend-confirm-email',
        detail=False,
        url_name='resend-confirm-email',
    )
    def resend_confirm_email(self, request: Request):
        email = request.data.get('email', '')
        if not email:
            return Response(
                'Email not found',
                status=status.HTTP_400_BAD_REQUEST
            )
        user_email = validate_email(request.data.get('email', ''))
        user = self.get_user_for_confirm(email=user_email)

        send_email_verification(
            user=user,
            viewset_instance=self
        )
        return Response(
            'Confirm email sent',
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['email'])
    @action(
        methods=['POST', ],
        url_path='reset-password',
        detail=False,
        url_name='reset-password',
    )
    def reset_password(self, request: Request):
        user_email = validate_email(request.data.get('email', ''))

        user = self.get_user_for_confirm(email=user_email)

        send_email_reset_password(
            user=user,
            viewset_instance=self
        )
        return Response(
            'Confirm email sent',
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['email'])
    @action(
        methods=['GET', ],
        url_path='reset-password-confirm',
        detail=False,
        url_name='reset-password-confirm',
    )
    def reset_password_confirm(self, request: Request):
        user_id = get_user_id_from_cache(
            request.query_params.get('confirm_token', ''),
            prefix_key=settings.IT_BEL_PASSWORD_RESET_CODE
        )
        if not user_id:
            return Response(
                'Token is invalid or expired. Please request/'
                ' another confirm email by signing in.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user: User = self.get_user_for_confirm(user_id=user_id)

        return Response(
            {'msg': 'Email confirmed', 'user_id': user.pk},
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['email'])
    @action(
        methods=['POST', ],
        url_path='set-new-password',
        detail=False,
        url_name='set-new-password',
    )
    def set_new_password(self, request: Request):
        user_id = request.data.get('user_id', '')
        new_password = request.data.get('new_password', '')
        if not user_id or not new_password:
            return Response(
                'User_id or new_password not found',
                status=status.HTTP_400_BAD_REQUEST
            )
        user: User = self.get_user_for_confirm(user_id=user_id)

        user.set_password(new_password)
        user.save()
        return Response(
            'Password changed',
            status=status.HTTP_200_OK
        )
