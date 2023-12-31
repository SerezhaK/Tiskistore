from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Название тега',
    )
    slug = models.SlugField(
        verbose_name='slug тега',
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['-id']

    def __str__(self) -> str:
        return self.name
