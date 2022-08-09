from django.db import models

# Create your models here.


from authapp.models import MyHabrUser


class BlogCategories(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")

    def __str__(self):
        return self.name



class Blogs(models.Model):
    DELETED = "0"
    PUBLISHED = '1'

    BLOG_STATUS = (
        (DELETED, 'блог удалена'),
        (PUBLISHED, 'блог опубликован'),

    )

    user = models.ForeignKey(MyHabrUser, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="название")
    status = models.CharField(max_length=1, choices=BLOG_STATUS, default=PUBLISHED, verbose_name="статус блога")
    def __str__(self):
        return self.name
