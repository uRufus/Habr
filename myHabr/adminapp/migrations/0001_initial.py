# Generated by Django 3.2.8 on 2022-08-01 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.CharField(max_length=150, verbose_name='автор сообщения')),
                ('text', models.TextField(blank=True, null=True, verbose_name='сообщение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('type_message', models.CharField(choices=[('0', 'Пользовательское сообщение'), ('1', 'На модерацию'), ('2', 'Ответ модератора'), ('3', 'Модератору')], default='0', max_length=1, verbose_name='Тип сообщения')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='адресат сообщения')),
            ],
            options={
                'db_table': 'messages',
            },
        ),
    ]
