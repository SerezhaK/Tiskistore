import random

from django.conf import settings
from django.core.cache.backends.locmem import LocMemCache
from django_redis.cache import RedisCache
from smsru.service import SmsRuApi

from users.models.user import User

if not settings.DOCKER:
    cache = LocMemCache('unique-snowflake', {})
else:
    cache = RedisCache('redis://redis:6379/1', {})


def get_redis_key_from_cache(user: User):
    user_info = cache.get(user.user_id) or None
    if user_info:
        return user_info.get('redis_key')
    return user_info


def get_new_password_from_cache(user: User):
    user_info = cache.get(user.user_id) or {}
    if user_info:
        return user_info.get('new_password')
    return user_info


def send_phone_number_verification(
        user: User,
        viewset_instance,
        new_password=None
):
    redis_key = str(random.randint(100000, 9999999))
    cache.set(
        user.user_id,
        {'redis_key': redis_key,
         'new_password': new_password
         },
        timeout=settings.TISKI_STORE_USER_CONFIRM_TIMEOUT
    )
    message = f"Код подтверждения: {redis_key} \n Никому не сообщайте!"
    user_phone_number = user.phone_number.as_e164
    api = SmsRuApi()
    api.send_one_sms(
        user_phone_number,
        message
    )
    return message
