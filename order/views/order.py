from rest_framework.viewsets import ModelViewSet

from cart.models.cart import Cart
from order.models.item import Item
from order.models.order import Order
from order.permissions import UserOwner
from order.serializers.order import OrderSerializer
from users.models.user import User


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [UserOwner]

    def perform_create(self, serializer: OrderSerializer):
        user: User = self.request.user
        order = serializer.save(user=user)
        carts = Cart.objects.filter(user=self.request.user)
        for cart in carts:
            Item.objects.create(
                product=cart.product,
                amount=cart.amount,
                order=order,
            )
            cart.delete()
        return order
