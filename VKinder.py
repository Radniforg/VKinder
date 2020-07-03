from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
from User_decomposition import user_interests
from User_decomposition import user_element_weight
from pprint import pprint
from data_procession import profile_pictures
import json



if __name__ == '__main__':
    TOKEN = '3641a1ff8ec80f2277ae1a29b0e7cc18054e6f07c367e621f2eee4c59dc8de6cf9afd5291a638752c6ca2'
    APP_ID =  7527992
    user = 6293784
    token_confirmation(APP_ID, TOKEN)
    user_confirmed(6293784, TOKEN)
    # pprint(user_interests(user, TOKEN))
    # pprint(user_element_weight())
    pprint(profile_pictures(user, TOKEN))
