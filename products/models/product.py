# from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from .category import Category
from .tag import Tag


class Product(models.Model):
    product_id = models.AutoField(
        primary_key=True,
        verbose_name='ID товара',
    )
    name = models.TextField(
        max_length=300,
        verbose_name='Название товара',
    )
    description = models.TextField(
        max_length=300,
        verbose_name='Описание товара',
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата добавления',
        help_text="date of joined in format dd.mm.yyyy",
    )
    last_modified_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата последнего изменения',
        help_text="date of last changes in format dd.mm.yyyy",
    )
    price = models.FloatField(
        verbose_name='Цена товара',
    )
    quantity = models.FloatField(
        verbose_name='Колличество товара',
    )
    product_image = models.ImageField(
        upload_to='covers/',
        verbose_name="Фото",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        blank=True
    )

    def __str__(self):
        return self.name

    def get_date(self):
        return self.date_joined.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-date_joined']
