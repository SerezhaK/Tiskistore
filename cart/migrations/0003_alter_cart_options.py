# Generated by Django 4.2.2 on 2023-12-12 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={
                "ordering": ["-product"],
                "verbose_name": "Корзина",
                "verbose_name_plural": "Корзина",
            },
        ),
    ]