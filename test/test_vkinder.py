import unittest
import VK_TOKEN as vt
import User_decomposition as ud
import data_procession as dp
import test_data
import settings as se

APP_ID = se.app_id
current_token = se.token
current_token = vt.token_confirmation(APP_ID, current_token)
vt.token_settings_save('../settings.py', current_token)


class vk_token_test(unittest.TestCase):
    def SetUp(self):
        pass

    def test_negative_settings_change(self, pathfile = '../setting.py', token = current_token):
        self.assertRaises(FileNotFoundError, lambda: vt.token_settings_save(pathfile, token))

class ud_Test(unittest.TestCase):
    def SetUp(self):
        pass

    def test_user_interests(self, user_id='4243253', token=current_token):
        elements_test = ud.user_interests(user_id, token)
        self.assertIs(type(elements_test), dict)

    def test_negative_user_ui(self, user_id='hgj897hjk', token=current_token):
        self.assertRaises(KeyError, lambda: ud.user_interests(user_id, token))

    def test_negative_token_ui(self, user_id='4243253', token=''):
        self.assertRaises(KeyError, lambda: ud.user_interests(user_id, token))

    def test_user_comparison(self):
        comparison = ud.user_comparison(ud.user_interests(test_data.friends[0], current_token),
                                        ud.user_interests(test_data.friends[1], current_token), test_data.matrix)
        self.assertIs(type(comparison), dict)

    def test_negative_user_comparison(self):
        self.assertRaises(TypeError,
                          lambda: ud.user_comparison(ud.user_interests(test_data.friends[0], current_token),
                                                     '', test_data.matrix))


class dp_Test(unittest.TestCase):
    def SetUp(self):
        pass

    def test_profile_picture(self):
        profile = dp.profile_pictures('4243253', current_token)
        self.assertIs(type(profile), list)

    def test_negative_profile_picture(self):
        self.assertIsNone(dp.profile_pictures('', current_token))

    def test_negative_token_error(self):
        self.assertIsNone(dp.profile_pictures('', ''))

    def test_partner_list(self):
        friend_list = []
        for friend in test_data.friends:
            friend_tuple = (vt.user_confirmed(friend, current_token), 0)
            friend_list.append(friend_tuple)
        result = dp.partner_photo(friend_list, current_token)
        self.assertIs(type(result), list)

    def test_negative_partner_photo_list(self):
        self.assertIsNone(dp.partner_photo([], current_token))

