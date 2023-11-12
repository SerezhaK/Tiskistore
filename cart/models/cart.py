from django.db import models

from users.models.user import User

from products.models.product import Product


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    amount = models.PositiveIntegerField(
        'Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'product')

    def __str__(self):
        return f'Корзина покупок {self.user.email}'

    def total_price(self) -> float:
        return self.amount * self.product.price
