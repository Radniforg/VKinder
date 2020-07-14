import user_decomposition as ud
from pprint import pprint
import data_procession as dp
import vkinder_sql as vs
import psycopg2 as pg
import settings as se
import json
import vk_token as vt
import sys


if __name__ == '__main__':
    current_token = vt.token_confirmation(se.app_id, se.token)
    current_user = vt.user_confirmed(se.user_id, current_token)
    if not current_user:
        sys.exit()
    user_information = ud.user_lesser_profile(current_token, current_user)
    standart = ud.user_element_weight()
    search_queue = {'city': user_information['city'],
                    'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart['sex_preference'],
                    'relation': standart['relation_ban'],
                    'age_limit': int(standart['age_limit'])}
    giant_id_list = dp.user_search(search_queue, current_token, [])
    with pg.connect(database=se.sql['database'], user=se.sql['username'],
                    password=se.sql['password']) as conn:
        ban_list = vs.block_check(conn, current_user).split(', ')
        sorted_partner_list = dp.partner_list(ban_list, user_information,
                                           giant_id_list, standart, current_token)
        vs.partner_add_block(conn, current_user, vs.new_ban(sorted_partner_list))
        results = dp.partner_photo(sorted_partner_list, current_token)
        pprint(results)
        vs.sql_result(conn, se.user_id, json.dumps(results))
    with open('partners.json', 'w') as res:
        json_in_file = json.dump(results, res)
