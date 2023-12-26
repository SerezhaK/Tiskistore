from rest_framework import serializers

from cart.models.cart import Cart
from products.models.product import Product
from products.serializers.products import ProductsSerializer
from users.serializers.users import UserListSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=False, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'product',
            'amount',
            'total_price',
            'user_total_price'
        )


class CartDetailSerializer(serializers.Serializer):
    user = UserListSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Product.objects.all()
    )
    amount = serializers.IntegerField(
        required=True,
        label='Количество',
    )

    class Meta:
        model = Cart
        fields = (
            'user',
            'product',
            'amount',
        )

    # def validation(self):
    #     amount = self.contex['request'].amount
    #     if amount <= 0:
    #         raise ValidationEr
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        amount = validated_data['amount']
        validated_data['user_id'] = user.user_id

        existed = Cart.objects.filter(user=user, product=product)
        if existed:
            existed = existed[0]
            existed.amount += amount
            if existed.amount <= 0:
                existed.delete()
                return existed
            existed.save()
        else:
            if amount <= 0:
                validated_data['amount'] = 1
                existed = Cart.objects.create(**validated_data)
                existed.delete()
            existed = Cart.objects.create(**validated_data)
        return existed
