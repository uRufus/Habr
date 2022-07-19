from django.db import models

# Create your models here.

class Profile(models.Model):
    # Пока что значение этого поля Число в дальней шем надо будет связать со связью 1-1 с таблицей users
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    text = models.TextField()