# Generated by Django 3.2.8 on 2022-07-21 20:28

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
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='CommentsLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('comment', 'комментарий'), ('article', 'статья'), ('blog', 'блог')], max_length=20)),
                ('assigned_id', models.IntegerField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.comment')),
            ],
            options={
                'db_table': 'comments_link',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('tag', models.CharField(max_length=30, verbose_name='тег')),
                ('category', models.CharField(max_length=255, verbose_name='категория')),
                ('body', models.TextField(verbose_name='текст статьи')),
                ('status', models.CharField(choices=[('0', 'статья удалена'), ('1', 'черновик'), ('2', 'статья на проверке'), ('3', 'обубликован'), ('4', 'статья заблокирована')], default='1', max_length=1, verbose_name='статус блогпоста')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'пост',
            },
        ),
    ]