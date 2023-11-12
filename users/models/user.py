from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from ..managers.user import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""

    user_id = models.AutoField(
        primary_key=True,
        verbose_name="ID пользователя"
    )
    username = models.CharField(
        verbose_name="Фамилия Имя пользователя",
        max_length=150,
        null=True,
        blank=True
    )
    email = models.EmailField(
        blank=False,
        null=False,
        verbose_name="Почта пользователя",
        help_text="Email",
        unique=True,
    )
    phone_number = PhoneNumberField(
        blank=False,
        null=False,
        verbose_name="Номер пользователя",
        help_text="phone number in format +71234567890",
        unique=True,
    )
    date_joined = models.DateTimeField(
        verbose_name="Дата регистрации",
        default=timezone.now,
    )
    is_staff = models.BooleanField(
        verbose_name="Админ",
        default=False
    )
    is_active = models.BooleanField(
        verbose_name="Активный",
        default=True
    )

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"

    def get_date(self):
        return self.date_joined.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['-date_joined']
