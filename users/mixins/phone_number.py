from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
import datetime
from ..models.user import User
from phone_activation.models import Phone_date
from ..services.phone_number import send_phone_number_verification


class PhoneNumberMixin:
    def get_user_for_confirm(self, user_id: int = None, phone_number: str = None):
        if user_id:
            return get_object_or_404(User, user_id=user_id)
        return get_object_or_404(User, phone_number=phone_number)

    def controle_code_validation(self, user, control_code):
        data = Phone_date.objects.get(user=user)
        if not data or not control_code:
            return Response(
                'Код не найден',
                status=status.HTTP_400_BAD_REQUEST
            )
        if data.activation_time + 60 * 15 < datetime.now():
            return Response(
                'Время для активации вышло, попробуйте еще раз',
                status=status.HTTP_400_BAD_REQUEST
            )
        if data.control_code != control_code:
            return Response(
                'Код не верный, попробуйте еще раз',
                status.HTTP_400_BAD_REQUEST
            )
        return control_code

    @action(
        methods=['POST'],
        url_path='activation',
        detail=False,
        url_name='activation',
    )
    def activation(self, request):
        control_code = self.controle_code_validation(
            user=request.request.data['user'],
            control_code=request.data.get('control_code', '')
        )
        user: User = self.get_user_for_confirm(user_id=request.data['user_id'])
        user.is_active = True
        user.save()
        return Response(
            'Успешно!',
            status=status.HTTP_200_OK,
        )

    # def get_user_for_confirm(self, user_id: int = None, phone_number: str = None):
    #     if user_id:
    #         return get_object_or_404(User, user_id=user_id)
    #     return get_object_or_404(User, phone_number=phone_number)
    #
    # @action(
    #     methods=["POST"],
    #     permission_classes=[AllowAny]
    # )
    # def generate_code(self, request):
    #     email = request.data['email']
    #     if Company.objects.filter(email=email).count() > 0:
    #         return Response(status=status.HTTP_302_FOUND,
    #                         data={'message': "Company with email '%s' is already registered." % email})
    #     code = str(random.randint(10000, 99999))
    #     ttl = cache.ttl(email + "_")
    #     if ttl > 0:
    #         return Response(status=status.HTTP_302_FOUND,
    #                         data={'message': 'You can generate code again after %s seconds.' % ttl})
    #     try:
    #         server.sendmail(from_address, email, code)
    #     except:
    #         server.login(username, password)
    #         server.sendmail(from_address, email, code)
    #     cache.set(email, code, timeout=3600 * 5)
    #     cache.set(email + "_", code, timeout=30)
    #     return Response(status=status.HTTP_200_OK, data={'message': 'Code is generated. %s' % code})
    #
    # # Check for code sent by company
    # @list_route(methods=["POST"], permission_classes=[AllowAny])
    # def check_code(self, request):
    #     cache_code = cache.get(request.data['email'])
    #     if cache_code == request.data['code']:
    #         serializer = CompanySerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(status=status.HTTP_200_OK, data={'message': 'Good job, your request is sent to admin.'})
    #     if cache_code is None:
    #         return Response(status=status.HTTP_404_NOT_FOUND,
    #                         data={'message': "There is no code for email '%s'" % request.data['email']})
    #     return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'Wrong code.'})
    #
    # @extend_schema(tags=['phone-number'])
    # @action(
    #     methods=['POST'],
    #     url_path='resend-confirm-phone-number',
    #     detail=False,
    #     url_name='resend-confirm-phone-number',
    # )
    # def resend_confirm_email(self, request: Request):
    #     phone_number = request.data.get('phone_number', '')
    #     if not phone_number:
    #         return Response(
    #             'phone number not found',
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     phone_number = validate_email(request.data.get('phone_number', ''))
    #     user = self.get_user_for_confirm(phone_number=phone_number)
    #     start_time = timezone.now()
    #     control_value = Random.randit(100000, 999999)
    #     send_phone_number_verification(
    #         control_value=control_value,
    #         user=user,
    #         viewset_instance=self
    #     )
    #     return Response(
    #         'Confirm email sent',
    #         status=status.HTTP_200_OK
    #     )
    #
    # @extend_schema(tags=['email'])
    # @action(
    #     methods=['POST', ],
    #     url_path='reset-password',
    #     detail=False,
    #     url_name='reset-password',
    # )
    # def reset_password(self, request: Request):
    #     user_email = validate_email(request.data.get('email', ''))
    #
    #     user = self.get_user_for_confirm(email=user_email)
    #
    #     send_email_reset_password(
    #         user=user,
    #         viewset_instance=self
    #     )
    #     return Response(
    #         'Confirm email sent',
    #         status=status.HTTP_200_OK
    #     )
    #
    # @extend_schema(tags=['email'])
    # @action(
    #     methods=['GET', ],
    #     url_path='reset-password-confirm',
    #     detail=False,
    #     url_name='reset-password-confirm',
    # )
    # def reset_password_confirm(self, request: Request):
    #     user_id = get_user_id_from_cache(
    #         request.query_params.get('confirm_token', ''),
    #         prefix_key=settings.IT_BEL_PASSWORD_RESET_CODE
    #     )
    #     if not user_id:
    #         return Response(
    #             'Token is invalid or expired. Please request/'
    #             ' another confirm email by signing in.',
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     user: User = self.get_user_for_confirm(user_id=user_id)
    #
    #     return Response(
    #         {'msg': 'Email confirmed', 'user_id': user.pk},
    #         status=status.HTTP_200_OK
    #     )
    #
    # @extend_schema(tags=['email'])
    # @action(
    #     methods=['POST', ],
    #     url_path='set-new-password',
    #     detail=False,
    #     url_name='set-new-password',
    # )
    # def set_new_password(self, request: Request):
    #     user_id = request.data.get('user_id', '')
    #     new_password = request.data.get('new_password', '')
    #     if not user_id or not new_password:
    #         return Response(
    #             'User_id or new_password not found',
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     user: User = self.get_user_for_confirm(user_id=user_id)
    #
    #     user.set_password(new_password)
    #     user.save()
    #     return Response(
    #         'Password changed',
    #         status=status.HTTP_200_OK
    #     )
