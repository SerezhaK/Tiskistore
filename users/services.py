import uuid

from django.conf import settings
from django.core.cache.backends.locmem import LocMemCache
from django.core.mail import send_mail
from django_redis.cache import RedisCache

from users.models.user import User

if not settings.DOCKER:
    cache = LocMemCache('unique-snowflake', {})
else:
    cache = RedisCache('redis://redis:6379/1', {})


def get_user_id_from_cache(token: str, prefix_key: str):
    redis_key = prefix_key.format(token=token)
    user_info = cache.get(redis_key) or {}
    return user_info.get('user_id', None)


def send_email_verification(user: User, viewset_instance):
    token = uuid.uuid4().hex
    redis_key = settings.TISKISTORE_USER_CONFIRM_KEY.format(
        token=token
    )
    cache.set(
        redis_key,
        {'user_id': user.pk},
        timeout=settings.TISKISTORE_USER_CONFIRM_TIMEOUT
    )
    # reverse_action возвращает http://back, пока им не пользуемся
    confirm_link_url = viewset_instance.reverse_action(  # noqa
        url_name='confirm',
        request=viewset_instance.request,
    )
    confirm_link = (f'http://127.0.0.1/api/users/confirm/?'
                    f'confirm_token={token}&user_id={user.pk}')
    message = f'Confirm your email: {confirm_link}'
    send_mail(
        subject='Confirm your email',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )


def send_email_reset_password(user: User, viewset_instance):
    token = uuid.uuid4().hex
    redis_key = settings.TISKISTORE_PASSWORD_RESET_CODE.format(
        token=token
    )
    cache.set(
        redis_key,
        {'user_id': user.pk},
        timeout=settings.TISKISTORE_USER_CONFIRM_TIMEOUT
    )
    # reverse_action возвращает http://back, пока им не пользуемся
    confirm_link_url = viewset_instance.reverse_action(  # noqa
        url_name='confirm',
        request=viewset_instance.request,
    )
    confirm_link = (f'http://127.0.0.1/api/users/reset-password-confirm/?'
                    f'confirm_token={token}&user_id={user.pk}')
    message = f'For set new password go to the link: {confirm_link}'
    send_mail(
        subject='Reset password',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
