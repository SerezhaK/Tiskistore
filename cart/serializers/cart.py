from rest_framework import serializers

from cart.models.cart import Cart
from products.models.product import Product
from products.serializers.products import ProductsSerializer
from users.serializers.users import UserListSerializer
from rest_framework.response import Response
from rest_framework import status


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

    # def validation_amount(self, amount, user, products):
    #     if Cart.objects.filter(user=user, product=products):
    #         return amount
    #     if amount > 0:
    #         return amount
    #     return serializers.ValidationError('This field must be an even number.')

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        amount = validated_data['amount']
        validated_data['user_id'] = user.user_id

        existed = Cart.objects.filter(user=user, product=product)
        # self.validation_amount( amount, user, product)
        if existed:
            existed = existed[0]
            existed.amount += amount
            if existed.amount <= 0:
                existed.delete()
                return existed
            existed.save()
        elif not int(validated_data['amount']) <= 0:
            existed = Cart.objects.create(**validated_data)
            return existed
        return existed

    def update(self, instance, validated_data):
        """ Изменение количества товара в корзине
        """

        instance.amount = validated_data['amount']
        instance.save()
        return instance
