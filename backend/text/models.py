# Create your models here.

from django.db import models


class Text(models.Model):
    text_id = models.AutoField(
        primary_key=True,
        verbose_name='ID текста',
    )
    name = models.TextField(
        max_length=300,
        verbose_name='Название текста',
    )
    text = models.TextField(
        max_length=300,
        verbose_name='Текст',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"
