from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cart.models.cart import Cart
from order.models.item import Item
from order.models.order import Order
from order.permissions import UserOwner
from order.serializers.order import OrderSerializer, OrderListSerializer
from users.models.user import User
from users.permissions import IsStuff


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

    @action(
        methods=['GET'],
        url_path='order_status',
        detail=False,
        permission_classes=[AllowAny],
    )
    def get_order_status_choise(self, request: Request):
        return Response({'order_status': (
            "Ожидает оплаты",
            "Создание транзакции",
            "Закрыт",
            "Время оплаты вышло"
        )},
            status=200)

    @action(
        methods=['GET'],
        url_path='all_orders',
        detail=False,
        permission_classes=[IsStuff],
    )
    def get_all_users_order(self, request: Request):
        self.serializer = OrderListSerializer()
        orders = Order.objects.all()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=200)
