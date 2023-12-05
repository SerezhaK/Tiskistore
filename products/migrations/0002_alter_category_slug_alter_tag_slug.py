# Generated by Django 4.2.2 on 2023-12-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(unique=True, verbose_name="slug категории"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(unique=True, verbose_name="slug тега"),
        ),
    ]
