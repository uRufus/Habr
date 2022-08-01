from django.db import models
from authapp import models as mod
# Create your models here.

class Profile(models.Model):
    # Связываем user_id с таблицей MyHabrUser с момошью связи 1 к 1.
    user_id = models.OneToOneField(to=mod.MyHabrUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    text = models.TextField()
    update_profile = models.BooleanField(default=False)