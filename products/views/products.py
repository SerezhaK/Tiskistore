from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from ..models.products import Product
from products.serializers.products import ProductsSerializer


class ProductsViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.prefetch_related(
         'tags'
    )
    serializer_class = ProductsSerializer
    # permission_classes = []
    # filter_backends = []
    # search_fields = ['title']