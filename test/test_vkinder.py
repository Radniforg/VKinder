import unittest
from unittest.mock import patch
import VKinder as vk
import VK_TOKEN as vt
import User_decomposition as ud
import data_procession as dp

APP_ID = 7527992
current_token = '4d807377c115c291c25cf1a2f3bde6c5be7a612b5490b28c2d816191790cc149fb6d42f01015d214c454c'

class Vkinder_Test(unittest.TestCase):
    pass

class ud_Test(unittest.TestCase):
    def SetUp(self):
        pass

    def test_user_interests(self, user_id = '4243253', token = current_token):
        elements_test = ud.user_interests(user_id, token)
        self.assertIs(type(elements_test), dict)

    def test_negative_user_ui(self, user_id = 'hgj897hjk', token = current_token):
        self.assertRaises(KeyError, lambda: ud.user_interests(user_id, token))

    def test_negative_token_ui(self, user_id = '4243253', token = ''):
        self.assertRaises(KeyError, lambda: ud.user_interests(user_id, token))

    def test_user_comparison(self, user_id_1, user_id_2, token, standart_matrix):
        pass


class dp_Test(unittest.TestCase):
    pass