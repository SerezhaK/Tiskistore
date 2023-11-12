from rest_framework import serializers

from products.models.category import Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
