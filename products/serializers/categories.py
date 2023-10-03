from rest_framework import serializers

from products.models.categories import Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
