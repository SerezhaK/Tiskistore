from rest_framework.viewsets import ModelViewSet

from cart.models.cart import Cart
from order.models.order import Order
from users.models.user import User
from order.models.item import Item
# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
# from rest_framework.request import HttpRequest
# from rest_framework.response import Response
# from rest_framework import status
# from cart.cart import Cart
from order.permissions import UserOwner
from order.serializers.item import ItemSerializer
# from products.models.product import Product
from order.serializers.order import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [UserOwner]

    # parser_classes = (parsers.MultiPartParser,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

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
