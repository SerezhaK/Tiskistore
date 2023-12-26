from rest_framework import mixins, permissions, viewsets

from ..models.cart import Cart
from ..serializers.cart import CartDetailSerializer, CartSerializer


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
