from rest_framework import serializers

from .models import Text


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('text', 'name', 'text_id')
