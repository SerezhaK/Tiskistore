from rest_framework import serializers
from datetime import datetime
import random
from order.models.order import Order
from users.serializers.users import UserListSerializer

from .item import ItemSerializer


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
        order = Order.objects.get(pk=instance.id)
        if order.status != validated_data['status'] and not self.context["request"].user.is_staff:
            raise serializers.ValidationError("Only admin can update status")
        return super().update(instance, validated_data)