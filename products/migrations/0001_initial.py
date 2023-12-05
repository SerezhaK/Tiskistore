# Generated by Django 4.2.2 on 2023-12-05 11:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                    "name",
                    models.CharField(max_length=64, verbose_name="Название категории"),
                ),
                ("slug", models.SlugField(verbose_name="slug категории")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=64, verbose_name="Название тега")),
                ("slug", models.SlugField(verbose_name="slug тега")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "product_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID товара"
                    ),
                ),
                (
                    "name",
                    models.TextField(max_length=300, verbose_name="Название товара"),
                ),
                (
                    "description",
                    models.TextField(max_length=300, verbose_name="Описание товара"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="date of joined in format dd.mm.yyyy",
                        verbose_name="Дата добавления",
                    ),
                ),
                (
                    "last_modified_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="date of last changes in format dd.mm.yyyy",
                        verbose_name="Дата последнего изменения",
                    ),
                ),
                ("price", models.FloatField(verbose_name="Цена товара")),
                ("quantity", models.FloatField(verbose_name="Колличество товара")),
                (
                    "product_image",
                    models.ImageField(upload_to="covers/", verbose_name="Фото"),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, to="products.category", verbose_name="Категория"
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, to="products.tag", verbose_name="Теги"
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
                "ordering": ["-date_joined"],
            },
        ),
    ]
