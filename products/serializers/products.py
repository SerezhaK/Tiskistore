from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ..models.categories import Category
from ..models.products import Product
from ..models.tag import Tag


class ProductsSerializer(serializers.ModelSerializer):
    product_image = Base64ImageField(required=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    added = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'product_id',
            'name',
            'description',
            'added',
            'last_modified_date',
            'price',
            'count',
            'product_image',
            'tags',
            'categories'
        ]

        read_only_fields = [
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        categories = validated_data.pop('categories')
        products = Product.objects.create(**validated_data)
        products.tags.set(tags)
        products.categories.set(categories)
        return products

    def get_added(self, obj: Product) -> str:
        return obj.get_date()
