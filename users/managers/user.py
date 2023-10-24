import unicodedata

from django.contrib.auth.models import UserManager as _UserManager
from django.db.transaction import atomic


class UserManager(_UserManager):
    def _create_user(
        self, email, username=None, password=None, **extra_fields
    ):

        if not password:
            raise ValueError("Пароль должен быть указан")

        if email:
            email = self.normalize_email(email)

        user = self.model(
            username=unicodedata.normalize(
                "NFKC", username or 'adminusername'),
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    @atomic
    def create_user(
        self, email, username=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            username=username, email=email, password=password, **extra_fields
        )

    @atomic
    def create_superuser(
        self, email, username=None, phone_number=None, password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(
            username=username, email=email, password=password, **extra_fields
        )
