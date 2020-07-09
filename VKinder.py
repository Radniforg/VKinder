from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
import User_decomposition as ud
from pprint import pprint
import data_procession as dp
import vkinder_sql as vs
import psycopg2 as pg
import json



if __name__ == '__main__':
    previous_token = 'bb3da54376b22e8b279faeb3a2fd081e72bb76f00e4de9e18a562f69e8f7817b4dbff8b08496961cb8486'
    APP_ID =  7527992
    user = 'grofindar'
    current_token = token_confirmation(APP_ID, previous_token)
    user_confirmed(user, current_token)
    user_information = ud.user_interests(user, current_token)
    standart = ud.user_element_weight()
    search_queue = {'city' : user_information['city'], 'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart['sex_preference'], 'relation': standart['relation_ban'],
                    'age_limit': standart['age_limit']}
    giant_id_list = []
    giant_id_list = dp.user_search(search_queue, current_token, giant_id_list)
    potential_partner_list = {}
    progress = 0
    with pg.connect(database = 'vkinder', user = 'vinder', password = 'vinder') as conn:
        print(vs.block_check(conn, user))
        ban_list = vs.block_check(conn, user).split(', ')
        for partner_id in giant_id_list:
            progress += 1
            if partner_id not in ban_list:
                raw_weight = ud.user_comparison(user_information, ud.user_interests(partner_id, current_token), standart)
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
        new_ban_list = ''
        for person in sorted_partner_list[:10]:
            new_ban_list = new_ban_list + ', ' + str(person[0])
        print('a')
        vs.partner_add_block(conn, user, new_ban_list)
        results = dp.partner_photo(sorted_partner_list, current_token)
        pprint(results)
        # vs.sql_result(conn, user, results)
        with open('partners.json') as res:
            json_in_file = json.load(results)
            pprint(results)
    #строка сортировки по весу
