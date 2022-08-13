from django.test import TestCase
from rest_framework import status
from rest_framework.test import *
from mixer.backend.django import mixer
# from .models import *
from profiles.models import *
from blogapp.models import *


class TestMainapp(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_name = 'John'
        self.user_pswd = 'Qwerty000'
        self.user_email = 'John@mail.ru'
        self.user = MyHabrUser.objects.create_user(username=self.user_name, password=self.user_pswd, email=self.user_email)
        self.author = mixer.blend(Profile)
        self.category = BlogCategories.objects.create(name='test_category')
        self.blog = Blogs.objects.create(user=self.user, category=self.category, name='test_blog')

    def test_create_post(self):
        self.client.login(username=self.user_name, password=self.user_pswd)
        self.client.get("/auth/login/")
        csrf_token = self.client.cookies['csrftoken'].value
        res = self.client.post('/blog/create/new/', data={
            'csrfmiddlewaretoken': csrf_token,
            'title': 'test_title',
            'blog': 1,
            'body': 'test_body',
            'tag_list': 'tag_test'
            })
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
