import uuid

from django.conf import settings
from django.core.cache.backends.locmem import LocMemCache
from django.core.mail import send_mail
from django.utils import timezone
from django_redis.cache import RedisCache
from phonenumber_field.phonenumber import PhoneNumber
from smsru.service import SmsRuApi

from users.models.user import User


def send_phone_number_verification(user: User, control_value, viewset_instance):
    message = f"Код подтверждения: {control_value} \n Никому не сообщайте!"
    user_phone_number = user.phone_number.as_e164
    api = SmsRuApi()
    api.send_one_sms(
        user_phone_number,
        message
    )
