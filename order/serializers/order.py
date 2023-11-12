from rest_framework import serializers

from order.models.order import Order
from users.serializers.users import UserListSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price']

    def update(self, instance, validated_data):
        order = Order.objects.get(pk=instance.id)
        if order.status != validated_data['status'] and\
                not self.context["request"].user.is_staff:
            raise serializers.ValidationError("Only admin can update status")
        return super().update(instance, validated_data)
