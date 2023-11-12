from rest_framework.viewsets import ModelViewSet

from order.models.order import Order
# from products.models.product import Product
from order.serializers.order import OrderSerializer

# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
# from rest_framework.request import HttpRequest
# from rest_framework.response import Response
# from rest_framework import status
# from cart.cart import Cart


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
