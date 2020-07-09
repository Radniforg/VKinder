from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
import User_decomposition as ud
from pprint import pprint
import data_procession as dp
import operator
import json



if __name__ == '__main__':
    previous_token = 'bb3da54376b22e8b279faeb3a2fd081e72bb76f00e4de9e18a562f69e8f7817b4dbff8b08496961cb8486'
    APP_ID =  7527992
    user = 'grofindar'
    current_token = token_confirmation(APP_ID, previous_token)
    user_confirmed(user, current_token)
    user_information = ud.user_interests(user, current_token)
    # partner_information = ud.user_interests(4243253, current_token)
    standart_matrix = ud.user_element_weight()
    pprint(user_information)
    # pprint(partner_information)
    # pprint(ud.user_comparison(user_information, partner_information, standart_matrix))
    search_queue = {'city' : user_information['city'], 'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart_matrix['sex_preference'], 'relation': standart_matrix['relation_ban'],
                    'age_limit': standart_matrix['age_limit']}
    giant_id_list = []
    giant_id_list = dp.user_search(search_queue, current_token, giant_id_list)
    potential_partner_list = {}
    progress = 0
    for partner_id in giant_id_list:
        progress += 1
        raw_weight = ud.user_comparison(user_information, ud.user_interests(partner_id, current_token), current_token)
        final_weight = 0
        if raw_weight:
            for value in raw_weight.values():
                if not value:
                    value = 0
                final_weight = final_weight + value
            potential_partner_list[partner_id] = final_weight
        print(f'{progress} потенциальных партнеров из {len(giant_id_list)} обработано')
    sorted_partner_list = sorted(potential_partner_list.items(), key=lambda x: x[1], reverse= True)
    pprint(sorted_partner_list)
    pprint(dp.partner_photo(sorted_partner_list, current_token, ban_list = []))
    #строка сортировки по весу
