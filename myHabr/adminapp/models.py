from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from authapp.models import MyHabrUser
# Create your models here.

class Message(models.Model):

    USER_TO_USER = '0'
    USER_TO_MODERATOR = '1'
    MODERATOR_TO_USER = '2'
    MODERATOR_TO_MODERATOR = '3'

    TYPE_MESSAGE = (
        (USER_TO_USER, 'Пользовательское сообщение'),
        (USER_TO_MODERATOR, 'На модерацию'),
        (MODERATOR_TO_USER, 'Ответ модератора'),
        (MODERATOR_TO_MODERATOR, 'Модератору'))

    from_user = models.CharField(max_length=150, null=True, blank=True, verbose_name="автор", default=None)
    to_user = models.ForeignKey(MyHabrUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="адресат")
    to_group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE, verbose_name="адресат(группа)")
    text = models.TextField(blank=True, null=True, verbose_name="сообщение")
    url = models.TextField(blank=True, null=True, verbose_name="Ссылка")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    type_message = models.CharField(max_length=1, choices=TYPE_MESSAGE, default=USER_TO_USER, verbose_name="Тип сообщения")
    is_read = models.BooleanField(default=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'messages'
        verbose_name = "Сообщение"
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'from_{self.from_user}|{self.created_at}'