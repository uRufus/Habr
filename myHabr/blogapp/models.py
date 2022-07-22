from django.db import models

# Create your models here.
from Habr.myHabr.mainapp.models import User


class BlogCategories:
    name = models.CharField(max_length=255, verbose_name="название")


class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    category = models.ForeignKey(BlogCategories, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, verbose_name="название")