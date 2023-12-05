# Generated by Django 4.2.2 on 2023-12-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveIntegerField(default=0, verbose_name="Количество"),
                ),
            ],
            options={
                "verbose_name": "Позиция заказа",
                "verbose_name_plural": "Позиции заказа",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("WAITING_FOR_PAYMENT", "Ожидает оплаты"),
                            ("CREATED_PAY", "Создание транзакции"),
                            ("DONE", "Закрыт"),
                            ("TIMEOUT", "Закрытие по таймауту"),
                        ],
                        default="WAITING_FOR_PAYMENT",
                    ),
                ),
                (
                    "order_number",
                    models.CharField(
                        max_length=17, unique=True, verbose_name="Номер заказа"
                    ),
                ),
                (
                    "order_comment",
                    models.CharField(
                        blank=True, max_length=1000, verbose_name="Комментарий к заказу"
                    ),
                ),
                (
                    "order_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время заказа"
                    ),
                ),
                (
                    "signer_firstname",
                    models.CharField(max_length=50, verbose_name="Имя заказчика"),
                ),
                (
                    "signer_lastname",
                    models.CharField(max_length=50, verbose_name="Фамилия заказчика"),
                ),
                (
                    "signer_address",
                    models.CharField(max_length=1000, verbose_name="Адрес доставки"),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "ordering": ["-order_time"],
            },
        ),
    ]
