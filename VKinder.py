from VK_TOKEN import token_confirmation
from VK_TOKEN import user_confirmed
import User_decomposition as ud
from pprint import pprint
import data_procession as dp
import vkinder_sql as vs
import psycopg2 as pg
import json


if __name__ == '__main__':
    previous_token = 'd8b724accc7c77fe5c3dc4018bf210af5304d1f70ad733c8cdf7e037c9a11eb2e318bbf3fe17588a91b00'
    APP_ID = 7527992
    current_token = token_confirmation(APP_ID, previous_token)
    user = user_confirmed('grofindar', current_token)
    user_information = ud.user_interests(user, current_token)
    standart = ud.user_element_weight()
    search_queue = {'city': user_information['city'],
                    'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart['sex_preference'],
                    'relation': standart['relation_ban'],
                    'age_limit': standart['age_limit']}
    giant_id_list = []
    giant_id_list = dp.user_search(search_queue, current_token, giant_id_list)
    potential_partner_list = {}
    progress = 0
    with pg.connect(database='vkinder', user='vinder',
                    password='vinder') as conn:
        ban_list = vs.block_check(conn, user).split(', ')
        for partner_id in giant_id_list:
            progress += 1
            if str(partner_id) not in ban_list:
                raw_weight = ud.user_comparison(user_information,
                                                ud.user_interests(partner_id, current_token),
                                                standart)
                final_weight = 0
                if raw_weight:
                    for value in raw_weight.values():
                        if not value:
                            value = 0
                        final_weight = final_weight + value
                    potential_partner_list[partner_id] = final_weight
                print(f'{progress} потенциальных партнеров'
                      f' из {len(giant_id_list)} обработано')
        sorted_partner_list = sorted(potential_partner_list.items(),
                                     key=lambda x: x[1], reverse=True)
        new_ban_list = ''
        for person in sorted_partner_list[:10]:
            new_ban_list = new_ban_list + ', ' + str(person[0])
        vs.partner_add_block(conn, user, new_ban_list)
        results = dp.partner_photo(sorted_partner_list, current_token)
        pprint(results)
        vs.sql_result(conn, user, json.dumps(results))
        with open('partners.json', 'w') as res:
            json_in_file = json.dump(results, res)
