import VK_TOKEN as vt
import User_decomposition as ud
from pprint import pprint
import data_procession as dp
import vkinder_sql as vs
import psycopg2 as pg
import settings as se
import json
import sys

def user_profile(token, username):
    previous_token = token
    APP_ID = se.app_id
    current_token = vt.token_confirmation(APP_ID, previous_token)
    user = vt.user_confirmed(username, current_token)
    if not user:
        sys.exit()
    user_info = ud.user_interests(user, current_token)
    user_info['bdate'] = ud.birthday(user_info)
    return user_info

if __name__ == '__main__':
    user_information = user_profile(se.token, se.user)
    standart = ud.user_element_weight()
    search_queue = {'city': user_information['city'],
                    'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart['sex_preference'],
                    'relation': standart['relation_ban'],
                    'age_limit': int(standart['age_limit'])}
    giant_id_list = dp.user_search(search_queue, se.token, [])
    potential_partner_list = {}
    progress = 0
    with pg.connect(database='vkinder', user='vinder',
                    password='vinder') as conn:
        ban_list = vs.block_check(conn, se.user).split(', ')
        for partner_id in giant_id_list:
            progress += 1
            if str(partner_id) not in ban_list:
                raw_weight = ud.user_comparison(user_information,
                                                ud.user_interests(partner_id, se.token),
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
        vs.partner_add_block(conn, se.user, new_ban_list)
        results = dp.partner_photo(sorted_partner_list, se.token)
        pprint(results)
        vs.sql_result(conn, se.user, json.dumps(results))
    with open('partners.json', 'w') as res:
        json_in_file = json.dump(results, res)
