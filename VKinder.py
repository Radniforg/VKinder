from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
import User_decomposition as ud
from pprint import pprint
import data_procession as dp
import itertools
import json



if __name__ == '__main__':
    previous_token = 'ceca3afaa04b570a2286f95199f8ecac5e03e94e302c20b38421187db42ba4b30576a21c7c6fa2ae1f30d'
    APP_ID =  7527992
    user = 'grofindar'
    current_token = token_confirmation(APP_ID, previous_token)
    user_confirmed(user, current_token)
    user_information = ud.user_interests(user, current_token)
    pprint(user_information)
    # search_queue = {'city' : user_information['city'], 'bdate': int(user_information['bdate'].split('.')[2]),
    #                 'sex': 0, 'relation': 0, 'age_limit': 5}
    # standart_matrix = ud.user_element_weight()
    # search_queue['sex'] = standart_matrix['sex_preference']
    # search_queue['relation'] = standart_matrix['relation_ban']
    # giant_id_list = []
    # giant_id_list = dp.user_search(search_queue, current_token, giant_id_list)
    # print(len(giant_id_list))
    # pprint(dp.data_preparation(user_information))
