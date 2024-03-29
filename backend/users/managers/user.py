import unicodedata

from django.contrib.auth.models import UserManager as _UserManager
from django.db.transaction import atomic
from phonenumber_field.phonenumber import PhoneNumber


class UserManager(_UserManager):

    def _create_user(
            self, phone_number, username=None, password=None, **extra_fields
    ):
        if phone_number:
            phone_number = PhoneNumber.from_string(
                phone_number=phone_number,
                region='RU'
            ).as_e164

        user = self.model(
            username=unicodedata.normalize(
                "NFKC",
                username or 'adminusername'),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    @atomic
    def create_user(
            self, phone_number, username=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)

        return self._create_user(
            username=username,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )

    @atomic
    def create_superuser(
            self, phone_number, username=None, password=None,
            **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)

        return self._create_user(
            username=username,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
