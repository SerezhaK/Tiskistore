from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404
from ..models.cart import Cart
from ..serializers.cart import CartDetailSerializer, CartSerializer
from products.models.product import Product
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework import mixins, viewsets
from django.core.exceptions import ValidationError


class CartViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet, ):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "product_id"
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CartSerializer
        else:
            return CartDetailSerializer

    def perform_create(self, serializer):
        product = self.request.query_params.get('product')
        queryset = Cart.objects.filter(user=self.request.user, product=product)
        if not queryset.exists():
            return Response("Нельзя добавить отрицательное колличество товара", status.HTTP_204_NO_CONTENT)
        serializer.save(user=self.request.user)