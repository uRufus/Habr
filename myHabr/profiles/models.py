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
