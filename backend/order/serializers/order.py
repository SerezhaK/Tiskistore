import random
from datetime import datetime

from rest_framework import serializers

from .item import ItemSerializer
from order.models.order import Order
from users.serializers.users import UserListSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    order_number = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    order_time = serializers.CharField(read_only=True)
    items = ItemSerializer(many=True, read_only=True)

    def generate_order_number(self):
        """ order number: current time + user id + random number(10, 99)
        """
        now = datetime.now()
        return '{time_now}{user_id}{random_int}'.format(
            time_now=now.strftime('%Y%m%d%H%M%S'),
            user_id=self.context['request'].user.user_id,
            random_int=random.randint(10, 99)
        )

    def validate(self, attrs):
        attrs['order_number'] = self.generate_order_number()
        return attrs

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'order_number',
            'status',
            'order_comment',
            'order_time',
            'items',
            'to_pay',
            'signer_firstname',
            'signer_lastname',
            'signer_address',
        ]

    def update(self, instance, validated_data):
        if not self.context["request"].user.is_staff:
            raise serializers.ValidationError("Only admin can update status")
        return super().update(instance, validated_data)


class OrderListSerializer(serializers.ModelSerializer):
    """ Сериализация информации о заказах в списке
    """

    order_number = serializers.CharField(read_only=True)
    order_status = serializers.CharField(read_only=True)
    order_time = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'order_time',
            'status',
            'to_pay',
        )
