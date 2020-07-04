from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
import User_decomposition as ud
from pprint import pprint
import data_procession as dp
import json



if __name__ == '__main__':
    TOKEN = '505deb0216ef6df79205599159c94a7ffc0a37b306281e8f33245280b0ba57b9d187713faebf732f23cfd'
    APP_ID =  7527992
    user = 6293784
    token_confirmation(APP_ID, TOKEN)
    user_confirmed(user, TOKEN)
    # pprint(ud.user_interests(user, TOKEN))
    # pprint(ud.user_element_weight())
    values = dp.data_preparation(ud.user_interests(user, TOKEN))
    pprint(dp.user_search(values, TOKEN))
