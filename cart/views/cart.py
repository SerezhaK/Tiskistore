from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404
from ..models.cart import Cart
from ..serializers.cart import CartDetailSerializer, CartSerializer
from products.models.product import Product
from rest_framework.response import Response
from rest_framework import status


class CartViewSet(viewsets.ModelViewSet):
    # parser_classes = (parsers.MultiPartParser,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CartSerializer
        else:
            return CartDetailSerializer

    # def perform_create(self, serializer: CartDetailSerializer):
    #     if not settings.PHONE_NUMBER_CONFIRM:
    #         serializer.save(is_active=True)
    #         return
    #     user = serializer.save(is_active=False)
    #     send_phone_number_verification(
    #         user=user,
    #         viewset_instance=self
    #     )
