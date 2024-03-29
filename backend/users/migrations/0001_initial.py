# Generated by Django 4.2.2 on 2024-02-18 10:53

from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields
import users.managers.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID пользователя')),
                ('username', models.CharField(max_length=150, verbose_name='Фамилия Имя пользователя')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text='phone number in format +79998887766', max_length=128, region=None, unique=True, verbose_name='Номер пользователя')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Админ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', users.managers.user.UserManager()),
            ],
        ),
    ]
