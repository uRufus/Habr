from django.test import TestCase
from rest_framework import status
from rest_framework.test import *
from mixer.backend.django import mixer

# from django.contrib.auth.models import User
from .views import *
from .models import *
from profiles.models import *


class TestAuthapp(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_name = 'John'
        self.user_pswd = 'Qwerty000'
        self.user_email = 'John@mail.ru'
        self.user = MyHabrUser.objects.create_user(username=self.user_name, password=self.user_pswd, email=self.user_email)
        self.author = mixer.blend(Profile)

    # def test_registrate(self):
    #     responce = self.client.post('/auth/register/', data={
    #         'username': 'Jo',
    #         'first_name': 'Bo',
    #         'password1': 'Qwerty000',
    #         'password2': 'Qwerty000',
    #         'email': 'jo@mail.ru'
    #     })
    #     self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_login_logout(self):
        # response = self.client.login(username=self.user_name, password=self.user_pswd)
        # self.assertTrue(response)
        self.client.post('/auth/login/', data={
            'username': 'John',
            'password': 'Qwerty0'
        })
        # self.client.login(username=self.user_name, password=self.user_pswd)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
        self.client.logout()
        # response = self.client.get('/')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_post_author(self):
    #     self.client.login(username=self.user_name, password=self.user_pswd)
    #     response = self.client.post('/profiles/', data={
    #         'first_name': "Паша",
    #         'last_name': 'Куманев',
    #         'birthday': 1900
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     author = Profile.objects.get(pk=response.data.get('id'))
    #     self.assertEqual(author.last_name, 'Куманев')
