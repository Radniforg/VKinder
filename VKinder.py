import user_decomposition as ud
from pprint import pprint
import data_procession as dp
import vkinder_sql as vs
import psycopg2 as pg
import settings as se
import json


if __name__ == '__main__':
    user_information = ud.user_profile(se.token, se.user)
    standart = ud.user_element_weight()
    search_queue = {'city': user_information['city'],
                    'bdate': int(user_information['bdate'].split('.')[2]),
                    'sex': standart['sex_preference'],
                    'relation': standart['relation_ban'],
                    'age_limit': int(standart['age_limit'])}
    giant_id_list = dp.user_search(search_queue, se.token, [])
    with pg.connect(database='vkinder', user='vinder',
                    password='vinder') as conn:
        ban_list = vs.block_check(conn, se.user).split(', ')
        sorted_partner_list = dp.partner_list(ban_list, user_information,
                                           giant_id_list, standart, se.token)
        vs.partner_add_block(conn, se.user, vs.new_ban(sorted_partner_list))
        results = dp.partner_photo(sorted_partner_list, se.token)
        pprint(results)
        vs.sql_result(conn, se.user, json.dumps(results))
    with open('partners.json', 'w') as res:
        json_in_file = json.dump(results, res)
