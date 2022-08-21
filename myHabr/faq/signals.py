from django.dispatch import receiver
from django.db.models.signals import post_save

from faq.models import Post


@receiver(post_save, sender=Post)
def post_save_user(created, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f'Статья {instance.title} создана')
    else:
        print(f'Статья {instance.title} обновлена')