from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class BlogUser(AbstractUser):
    admin = models.BooleanField()
    moderator = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()