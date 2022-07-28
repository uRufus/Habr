import sys
import os
from django.test import TestCase
from .authapp import  *
sys.path.append(os.path.join(os.getcwd(), '..'))


class LogInOutTest(unittest.TestCase):

    def setUp(self):
        self.client = register()

    def tearDown(self):
        pass

    def test_login(self):
        response = self.client.get('/login/')

        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log in' in response.content)

        self.client.login(username='John', password="John1234")

        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        self.client.login(username='John', password="John1234")

        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log out' in response.content)

        self.client.logout()

        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log in' in response.content)


if __name__ == '__main__':
    unittest.main()
