from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        verbose_name='slug категории'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name