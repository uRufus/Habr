import sys
import os
from django.test import TestCase
from .mainapp import  *
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestFaq(unittest.TestCase):
    def setUp(self):
        pass
    def testHome(self):
        pass