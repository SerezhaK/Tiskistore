from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from products.models.category import Category
from products.models.product import Product
from products.permissions import StaffUserOrReadOnly
from products.serializers.categories import CategoriesSerializer
from products.serializers.products import ProductsSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [StaffUserOrReadOnly]

    @action(
        methods=['GET', ],
        detail=True,
        url_path='products',
        permission_classes=[AllowAny]
    )
    def get_category_products(self, request: HttpRequest, pk: int):
        self.serializer_class = ProductsSerializer
        category = get_object_or_404(Category, id=pk)
        products = Product.objects.filter(categories=category)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
