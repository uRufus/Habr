# Generated by Django 3.2.14 on 2022-08-09 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='authapp.myhabruser')),
                ('first_name', models.CharField(blank=True, default='', max_length=50)),
                ('last_name', models.CharField(blank=True, default='', max_length=50)),
                ('age', models.PositiveSmallIntegerField(default=18)),
                ('text', models.TextField(blank=True, default='')),
                ('update_profile', models.BooleanField(default=False, editable=False)),
            ],
        ),
    ]
