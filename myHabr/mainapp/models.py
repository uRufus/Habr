from django.db import models
from django.conf import settings


from authapp.models import MyHabrUser
from blogapp.models import BlogCategories
from blogapp.models import Blogs

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="автор")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True,
                                   verbose_name="Лайк поста")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislikes', blank=True,
                                      verbose_name="Дизлайк поста")
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")
    blog = models.ForeignKey(Blogs, default='', on_delete=models.CASCADE, verbose_name="блог")
    body = models.TextField(verbose_name="текст статьи")
    # blog_id = bigint
    status = models.CharField(max_length=1, choices=BLOGPOST_STATUS, default=DRAFT, verbose_name="статус блогпоста")
    create_date = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name="дата создания")
    update_date = models.DateTimeField(null=False, blank=False, auto_now=True, verbose_name="дата обновления")

    def __str__(self):
        return f'{self.title}  |  {self.author}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

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


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='comment_user',
                             blank=True, null=True)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_children = models.BooleanField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True,
                                   verbose_name="Лайк комментария")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_dislikes', blank=True,
                                      verbose_name="Дизлайк комментария")

    class Meta:
        db_table = 'comments'
        verbose_name = "Комментарий"
        verbose_name_plural = 'Комментарии'

    def find_children(self):
        if not self.has_children:
            self.children = []
        else:
            self.children = (
                Comment.objects
                .filter(commentslink__type='comment',
                        commentslink__assigned_id=self.id)
            )
            if self.children:
                for child in self.children:
                    child.find_children()


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
