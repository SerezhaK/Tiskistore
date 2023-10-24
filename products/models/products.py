# from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from .categories import Category
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
    added = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата добавления',
    )
    last_modified_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата последнего изменения',
    )
    price = models.FloatField(
        verbose_name='Цена товара',
    )
    count = models.FloatField(
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
        return self.added.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-added']
