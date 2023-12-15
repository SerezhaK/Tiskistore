from rest_framework import serializers

from ..models.item import Item
from products.models.product import Product


class ItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Product.objects.all()
    )
    amount = serializers.IntegerField(
        required=True,
        label='Количество',
    )

    class Meta:
        model = Item
        fields = [
            'id',
            'product',
            'amount',
            'total_price',
        ]
