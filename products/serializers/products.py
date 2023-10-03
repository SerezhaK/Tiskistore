from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ..models.products import Product
from ..models.tag import Tag


class ProductsSerializer(serializers.ModelSerializer):
    # product_image = Base64ImageField(required=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Product
        fields = [
            'product_id',
            'name',
            'description',
            'added',
            'Last_modified_date',
            'price',
            'count',
            'tags'
        ]

        read_only_fields = [
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        products = Product.objects.create(**validated_data)
        products.tags.set(tags)
        return products
