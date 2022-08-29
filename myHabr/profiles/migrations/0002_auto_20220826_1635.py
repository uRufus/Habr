# Generated by Django 3.2.14 on 2022-08-26 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dislikes',
            field=models.IntegerField(default=0, editable=False, verbose_name='Количество дизлайков'),
        ),
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.IntegerField(default=0, editable=False, verbose_name='Количество лайков'),
        ),
        migrations.CreateModel(
            name='LikeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('how', models.CharField(choices=[('N', 'нет лайка'), ('L', 'лайк'), ('D', 'Дизлайк')], default='N', max_length=1, verbose_name='Как лайкнули')),
                ('to_whom_did', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_whom_did', to=settings.AUTH_USER_MODEL, verbose_name='Кого лайкнули')),
                ('who_did', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='who_did', to=settings.AUTH_USER_MODEL, verbose_name='Кто лайкнул')),
            ],
        ),
    ]
