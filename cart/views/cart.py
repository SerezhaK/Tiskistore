from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

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

    # def perform_create(self, serializer):
    #     product = self.request.query_params.get('product')
    #     queryset = Cart.objects.filter(user=self.request.user, product=product)
    #     serializer.save(user=self.request.user)
