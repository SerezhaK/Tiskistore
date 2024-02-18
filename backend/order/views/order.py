from django.shortcuts import get_object_or_404
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cart.models.cart import Cart
from order.models.item import Item
from order.models.order import Order
from order.permissions import UserOwner
from order.serializers.order import OrderListSerializer, OrderSerializer
from users.models.user import User
from users.permissions import IsStuff


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [UserOwner]
    lookup_field = 'pk'
    lookup_url_kwarg = 'order_time'

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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(
        methods=['GET'],
        url_path='order_status',
        detail=False,
        permission_classes=[AllowAny],
    )
    def get_order_status_choise(self, request: Request):
        return Response({'order_status': (
            "Ожидание звонка",
            "Ожидание оплаты",
            "Закрыт",
            "Время оплаты вышло"
        )},
            status=status.HTTP_200_OK)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        url_path='status_orders',
        detail=False,
        permission_classes=[IsStuff],
    )
    def get_all_status_order(self, request: Request):
        self.serializer = OrderListSerializer()
        if "status" not in request.data:
            return Response(
                "Ошибка, попробуйте еще раз."
                "Проверьте правильность заполненных полей",
                status=status.HTTP_200_OK
            )
        order_status = request.data["status"]
        orders = Order.objects.filter(status=order_status)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        url_path='by_phone_orders',
        detail=False,
        permission_classes=[IsStuff],
    )
    def get_order_by_phone_number(self, request: Request):
        self.serializer = OrderListSerializer()
        if "phone_number" not in request.data:
            return Response(
                "Ошибка, попробуйте еще раз."
                " Проверьте правильность заполненных полей",
                status=status.HTTP_200_OK
            )
        phone_number = request.data["phone_number"]
        phone_number_valid = PhoneNumber.from_string(
            phone_number=phone_number,
            region='RU'
        ).as_e164
        user = get_object_or_404(User, phone_number=phone_number_valid)
        orders = Order.objects.filter(user=user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
