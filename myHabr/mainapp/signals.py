from django.dispatch import receiver
from django.db.models.signals import post_save

from mainapp.models import Comment


@receiver(post_save, sender=Comment)
def post_save_user(created, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f'Пользователь {instance.user} создан')
    else:
        print(f'Пользователь {instance.user} обновлен')
