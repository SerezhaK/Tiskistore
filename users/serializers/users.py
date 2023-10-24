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
            "email",
            "username",
            "phone_number",
            "password",
            "date_joined",
        ]

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data: dict):
        if 'username' not in validated_data:
            validated_data['username'] = f'username{randint(1000000, 9999999)}'

        password = validated_data.pop('password')

        user = User.objects.create(
            **validated_data
        )

        try:
            user.set_password(password)
            user.save()
        except serializers.ValidationError as exc:
            user.delete()
            raise exc


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'date_joined', ]

    def get_date_joined(self, obj: User) -> str:
        return obj.get_date()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', "phone_number"]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
