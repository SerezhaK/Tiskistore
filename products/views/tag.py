from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from products.models.products import Product
from products.models.tag import Tag
from products.serializers.products import ProductsSerializer
from products.serializers.tag import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    # queryset = Tag.objects.prefetch_related('tags')
    serializer_class = TagSerializer

    # permission_classes = []
    # pagination_class = None

    @action(
        methods=['GET', ],
        detail=True,
        url_path='products',
    )
    def get_tag_products(self, request: HttpRequest, pk: int):
        self.serializer_class = ProductsSerializer
        tag = get_object_or_404(Tag, id=pk)
        products = Product.objects.filter(tags=tag)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
