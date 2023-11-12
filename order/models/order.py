from django.db import models

from cart.models.cart import Cart


class OrderStatusChoices(models.TextChoices):
    WAITING_FOR_PAYMENT = "WAITING_FOR_PAYMENT", "Ожидает оплаты"
    IN_PROGRESS = "IN_PROGRESS", "В процессе"
    DONE = "DONE", "Закрыт"


class Order(models.Model):
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.WAITING_FOR_PAYMENT
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='Корзина',
        blank=True
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        verbose_name='суммарная цена'

    )
    total_items = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='суммарное колличество'
    )

    def save(self, *args, **kwargs):
        self.total_price = sum(item.get_cost() for item in self.cart)
        self.total_items = sum(item.quantity for item in self.cart)
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
