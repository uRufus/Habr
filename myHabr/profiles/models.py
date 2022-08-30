from django.db import models
from authapp import models as mod


# Create your models here.

class Profile(models.Model):
    # Связываем user_id с таблицей MyHabrUser с момошью связи 1 к 1.
    user_id = models.OneToOneField(to=mod.MyHabrUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=True, default='')
    last_name = models.CharField(max_length=50, null=False, blank=True, default='')
    age = models.PositiveSmallIntegerField(default=18)
    text = models.TextField(null=False, blank=True, default='')
    update_profile = models.BooleanField(default=False, editable=False)
    image = models.ImageField(upload_to='profile_images', default='default_photo_profile.png')

    likes = models.IntegerField(default=0, verbose_name='Количество лайков', editable=False)
    dislikes = models.IntegerField(default=0, verbose_name='Количество дизлайков', editable=False)

class LikeProfile(models.Model):
    WHO_LIKE = (
        ('N', 'нет лайка'),
        ('L', 'лайк'),
        ('D', 'Дизлайк'),
    )

    who_did = models.ForeignKey(to=mod.MyHabrUser, on_delete=models.CASCADE, verbose_name='Кто лайкнул', related_name='who_did', blank=True)
    to_whom_did = models.ForeignKey(to=mod.MyHabrUser, on_delete=models.CASCADE, verbose_name='Кого лайкнули', related_name='to_whom_did', blank=True)
    how = models.CharField(choices=WHO_LIKE, default='N', verbose_name='Как лайкнули', max_length=1)