# Generated by Django 3.2.14 on 2022-08-09 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='status',
            field=models.CharField(choices=[('0', 'блог удалена'), ('1', 'блог опубликован')], default='1', max_length=1, verbose_name='статус блога'),
        ),
    ]
