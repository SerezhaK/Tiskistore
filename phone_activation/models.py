from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db import models
from users.models.user import User


class Phone_date(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='auth'
    )
    control_code = models.CharField(
        max_length=6,
        null=False,
        blank=False
    )
    activation_time = models.DateTimeField(
        verbose_name="Дата запроса подтверждения",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "Auth"
        ordering = ['-activation_time']
