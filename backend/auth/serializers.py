from djoser.serializers import TokenSerializer
from rest_framework import serializers


class CustomTokenSerializer(TokenSerializer):
    user_id = serializers.IntegerField(source='user.user_id')

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ('user_id',)
