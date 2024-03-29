from random import randint

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models.user import User


class UserCreateCustomSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'user_id',
            "username",
            "phone_number",
            "password",
            "date_joined",
        ]

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data: dict, is_admin=False):
        if 'username' not in validated_data:
            validated_data['username'] = f'username{randint(1000000, 9999999)}'

        password = validated_data.pop('password')

        if is_admin:
            user = User.objects.create_superuser(
                **validated_data
            )
            user.set_is_active = True
        else:
            user = User.objects.create(
                **validated_data
            )

        try:
            user.set_password(password)
            user.save()
            return user

        except serializers.ValidationError as exc:
            user.delete()
            raise exc

    def update(self, instance, validated_data):
        user = instance
        if "is_staff" in validated_data:
            user.is_staff = validated_data['is_staff']
        return super().update(instance, validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'date_joined',
            'is_staff',
            'phone_number',
            'is_active'
        ]

    def get_date_joined(self, obj: User) -> str:
        return obj.get_date()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "phone_number"]
