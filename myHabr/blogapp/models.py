from django.db import models

# Create your models here.


from authapp.models import MyHabrUser


class BlogCategories(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")

    def __str__(self):
        return f'{self.name}'


class Blogs(models.Model):
    user = models.ForeignKey(MyHabrUser, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="название")
