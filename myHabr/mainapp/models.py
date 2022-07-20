from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlogPost(models.Model):
    DELETED = "0"
    DRAFT = '1'
    UNDER_REVIEW = '2'
    PUBLISHED = '3'
    BLOCKED = '4'

    BLOGPOST_STATUS = (
        (DELETED, 'статья удалена'),
        (DRAFT, 'черновик'),
        (UNDER_REVIEW, 'статья на проверке'),
        (PUBLISHED, 'обубликован'),
        (BLOCKED, 'статья заблокирована'),

    )

    title = models.CharField(max_length=255, verbose_name="название")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    tag = models.CharField(max_length=30, verbose_name="тег")
    category = models.CharField(max_length=255, verbose_name="категория")
    body = models.TextField(verbose_name="текст статьи")
    status = models.CharField(max_length=1, choices=BLOGPOST_STATUS, default=DRAFT, verbose_name="статус блогпоста")
    create_date = models.DateField(auto_now_add=True, verbose_name="дата создания")
    update_date = models.DateField(auto_now=True, verbose_name="дата обновления")

    def __str__(self):
        return f'{self.title}  |  {self.author}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
