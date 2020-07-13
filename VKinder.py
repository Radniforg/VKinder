import user_decomposition as ud
from pprint import pprint
import data_procession as dp
import vkinder_sql as vs
import psycopg2 as pg
import settings as se
import json
import vk_token as vt


if __name__ == '__main__':
    user_information = ud.user_profile(se.token, se.user_id)
    standart = ud.user_element_weight()
    search_queue = {'city': user_information['city'],
                    'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart['sex_preference'],
                    'relation': standart['relation_ban'],
                    'age_limit': int(standart['age_limit'])}
    giant_id_list = dp.user_search(search_queue, vt.value_get('settings.py', 'token'), [])
    with pg.connect(database=se.sql['database'], user=se.sql['username'],
                    password=se.sql['password']) as conn:
        ban_list = vs.block_check(conn, vt.value_get('settings.py', 'user_id')).split(', ')
        sorted_partner_list = dp.partner_list(ban_list, user_information,
                                           giant_id_list, standart, vt.value_get('settings.py', 'token'))
        vs.partner_add_block(conn, vt.value_get('settings.py', 'user_id'), vs.new_ban(sorted_partner_list))
        results = dp.partner_photo(sorted_partner_list, vt.value_get('settings.py', 'token'))
        pprint(results)
        vs.sql_result(conn, se.user_id, json.dumps(results))
    with open('partners.json', 'w') as res:
        json_in_file = json.dump(results, res)
