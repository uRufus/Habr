from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


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
        (PUBLISHED, 'опубликован'),
        (BLOCKED, 'статья заблокирована'),

    )

    title = models.CharField(max_length=255, verbose_name="название")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    tag = models.CharField(max_length=30, verbose_name="тег")
    category = models.CharField(max_length=255, verbose_name="категория")
    body = models.TextField(verbose_name="текст статьи")
    status = models.CharField(max_length=1, choices=BLOGPOST_STATUS, default=DRAFT, verbose_name="статус блогпоста")
    create_date = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name="дата создания")
    update_date = models.DateTimeField(null=False, blank=False, auto_now=True, verbose_name="дата обновления")

    def __str__(self):
        return f'{self.title}  |  {self.author}'

    def delete(self, using=None, keep_parents=False):
        if self.status != "0":
            self.status = "0"
        else:
            self.status = "1"
        self.save()

    def send_verify(self):
        if self.status:
            if self.status == "1":
                self.status = "2"
        self.save()

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,
                             null=True)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'comments'

class CommentsLink(models.Model):
    types = (
        ('comment', 'комментарий'),
        ('article', 'статья'),
        ('blog', 'блог'),
    )
    type = models.CharField(max_length=20, choices=types, null=False,
                             blank=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                   null=False, blank=False)
    assigned_id = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'comments_link'
