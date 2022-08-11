from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class MyHabrUser(AbstractUser):
    pass


# class MyHabrUserProfile(models.Model):
#     MALE = 'M'
#     FEMALE = 'W'
#
#     GENDER_CHOICES = (
#         (MALE, 'М'),
#         (FEMALE, 'Ж'),
#     )
#
#     user = models.OneToOneField(MyHabrUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
#     tag_line = models.CharField(verbose_name='теги', max_length=128, blank=True)
#     about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)
#     gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
