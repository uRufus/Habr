# Generated by Django 3.2.14 on 2022-08-09 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(default='Описание')),
                ('keywords', models.CharField(default='Ключевые слова', max_length=120)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('content', models.TextField()),
                ('visible', models.BooleanField(default=1)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id', '-timestamp'],
            },
        ),
    ]
