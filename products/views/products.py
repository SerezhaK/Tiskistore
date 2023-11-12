from rest_framework import viewsets

from products.models.product import Product
from products.serializers.products import ProductsSerializer


class ProductsViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.prefetch_related(
         'tags', 'categories'
    )
    serializer_class = ProductsSerializer
    # permission_classes = []
    # filter_backends = []
    # search_fields = ['title']
