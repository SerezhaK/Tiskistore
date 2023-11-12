from rest_framework import permissions, viewsets

from ..models.cart import Cart
from ..serializers.cart import CartDetailSerializer, CartSerializer


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
