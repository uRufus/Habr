from django.contrib import admin
from authapp.models import MyHabrUser
from mainapp.models import BlogPost
# Register your models here.

admin.site.register(MyHabrUser)
admin.site.register(BlogPost)