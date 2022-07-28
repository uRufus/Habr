import sys
import os
from django.test import TestCase
from .faq import  *
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestFaq(unittest.TestCase):
    def setUp(self):
        pass
    def testHome(self):
        pass
    def test_200_ans(self):
        self.assertEqual((...), '200 : ok')

    def test_400_ans(self):
        self.assertEqual((...), '400 : Bad Request')

    def test_error_ans(self):
        self.assertRaises((...), 'Wrong dict')

    def test_str_ans(self):
        self.assertIsInstance((...), str)

    def test_no_dict_ans(self):
        self.assertNotIsInstance((...), dict)


if __name__ == '__main__':
    unittest.main()