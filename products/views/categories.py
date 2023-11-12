from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from products.models.category import Category
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from products.models.product import Product
from products.serializers.categories import CategoriesSerializer
from products.serializers.products import ProductsSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('products')
    # queryset = Tag.objects.prefetch_related('products')
    serializer_class = CategoriesSerializer

    # permission_classes = []
    # pagination_class = None

    @action(
        methods=['GET', ],
        detail=True,
        url_path='products',
    )
    def get_category_products(self, request: HttpRequest, pk: int):
        self.serializer_class = ProductsSerializer
        category = get_object_or_404(Category, id=pk)
        products = Product.objects.filter(categories=category)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
