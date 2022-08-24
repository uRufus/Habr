from django.test import TestCase
from rest_framework import status
from rest_framework.test import *
from mixer.backend.django import mixer
from django.urls import include, path, reverse

# from .views import *
from authapp import models as mod
from profiles.models import *


class TestAuthapp(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_name = 'John'
        self.user_pswd = 'Qwerty000'
        self.user_email = 'John@mail.ru'
        self.user = mod.MyHabrUser.objects.create_user(username=self.user_name, password=self.user_pswd, email=self.user_email)
        self.author = mixer.blend(Profile)

    def test_registrate(self):
        responce = self.client.post('/auth/register/', data={
            'username': 'Jo',
            'first_name': 'Bo',
            'password1': 'Qwerty000',
            'password2': 'Qwerty000',
            'email': 'jo@mail.ru'
        })
        self.assertEqual(responce.status_code, 302)

    def test_login_logout(self):
        response = self.client.login(username=self.user_name, password=self.user_pswd)
        self.assertTrue(response)
        self.client.post('/auth/login/', data={
            'username': 'John',
            'password': 'Qwerty0'
        })
        self.client.login(username=self.user_name, password=self.user_pswd)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mod.MyHabrUser.objects.count(), 2)
        # self.assertEqual(len(response.data), 1)
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_post_author(self):
    #     self.client.login(username=self.user_name, password=self.user_pswd)
    #     res = self.client.post('/profiles/create_update_profile/', data={
    #         'first_name': "Паша",
    #         'last_name': 'Куманев',
    #         'birthday': 1900,
    #         'name': '123'
    #     })
    #     self.assertEqual(res.status_code, 200)
    #     response = self.client.get('/profiles/create_update_profile/')
    #     author = Profile.objects.get(pk=response.data.get('id'))
    #     self.assertEqual(author.last_name, 'Куманев')
