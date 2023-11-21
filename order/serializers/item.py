from rest_framework import serializers

from ..models.item import Item
from products.serializers.products import ProductsSerializer


class ItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'product',
            'amount',
            'total_price',
        ]
