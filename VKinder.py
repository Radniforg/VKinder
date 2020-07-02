from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
from User_decomposition import user_interests
from User_decomposition import user_element_weight
from pprint import pprint
from data_procession import profile_pictures
import json



if __name__ == '__main__':
    TOKEN = 'fe2b853bb40a4e7eb972ff331052d1b3f8cba7e3cf1127829e75e76394309f05f1288723f01ae9a623799'
    APP_ID =  7527992
    user = 6293784
    token_confirmation(APP_ID, TOKEN)
    user_confirmed(6293784, TOKEN)
    # pprint(user_interests(user, TOKEN))
    # pprint(user_element_weight())
    pprint(profile_pictures(user, TOKEN))
