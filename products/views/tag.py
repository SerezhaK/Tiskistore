from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from products.models.product import Product
from products.models.tag import Tag
from products.permissions import StaffUserOrReadOnly
from products.serializers.products import ProductsSerializer
from products.serializers.tag import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [StaffUserOrReadOnly]

    @action(
        methods=['GET', ],
        detail=True,
        url_path='products',
        permission_classes=[AllowAny]
    )
    def get_tag_products(self, request: HttpRequest, pk: int):
        self.serializer_class = ProductsSerializer
        tag = get_object_or_404(Tag, id=pk)
        products = Product.objects.filter(tags=tag)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
