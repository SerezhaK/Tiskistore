from django.db import models

from users.models.user import User


class Order(models.Model):
    status = models.TextField(
        default="Ожидание звонка"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_number = models.CharField(
        'Номер заказа',
        max_length=17,
        unique=True
    )
    order_comment = models.CharField(
        'Комментарий к заказу',
        max_length=1000,
        blank=True
    )
    order_time = models.DateTimeField(
        'Время заказа',
        auto_now_add=True
    )

    signer_firstname = models.CharField(
        'Имя заказчика',
        max_length=50
    )
    signer_lastname = models.CharField(
        'Фамилия заказчика',
        max_length=50
    )
    signer_address = models.CharField(
        'Адрес доставки',
        max_length=1000
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_time']

    def __str__(self):
        return f'Заказ {self.order_number}'

    def to_pay(self) -> int:
        return sum(item.total_price() for item in self.items.all())
