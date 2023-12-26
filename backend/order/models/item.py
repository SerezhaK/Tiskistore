from django.db import models

from .order import Order
from products.models.product import Product


class Item(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        related_name='product_items',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        'Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product.id} - {self.product.title}'

    def total_price(self) -> float:
        return self.amount * self.product.price

    def user_total_price(self) -> float:
        return sum(
            [item.total_price()
             for item in Item.objects.filter(order=self.order)]
        )
