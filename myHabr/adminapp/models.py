from django.db import models
from django.conf import settings
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

    from_user = models.CharField(max_length=150, verbose_name="автор сообщения")
    to_user = models.ForeignKey(MyHabrUser, on_delete=models.DO_NOTHING, blank=True,
                             null=True, verbose_name="адресат сообщения")
    text = models.TextField(blank=True, null=True, verbose_name="сообщение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    type_message = models.CharField(max_length=1, choices=TYPE_MESSAGE, default=USER_TO_USER, verbose_name="Тип сообщения")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'messages'