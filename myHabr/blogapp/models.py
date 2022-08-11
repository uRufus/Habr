from django.db import models

# Create your models here.


from authapp.models import MyHabrUser


class BlogCategories(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name



class Blogs(models.Model):
    user = models.ForeignKey(MyHabrUser, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="название")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.name
