import time
import keyholder as ke
import user_decomposition as ud
import vk_token as vt


def profile_pictures(user_id, token):
    ke.profile['owner_id'] = user_id
    response_id = vt.request('https://api.vk.com/method/photos.get',
                             vt.parameters(token, ke.profile))
    print(f'Обрабатывается профиль пользователя id{user_id}')
    try:
        photo_data = response_id['response']['items']
    except KeyError:
        return None
    raw = []
    for profile_picture in photo_data:
        temp_dictionary = {'like': profile_picture['likes']['count'],
                           'date': profile_picture['date']}
        for size in profile_picture['sizes']:
            if size['type'] == 'x':
                temp_dictionary['url'] = size['url']
                break
        raw.append(temp_dictionary)
    raw.sort(reverse=True, key=lambda x: (x['like'], x['date']))
    profile = []
    if len(raw) >= 3:
        for i in range(3):
            profile.append(raw[i]['url'])
    elif len(raw) == 0:
        return None
    else:
        for i in range(len(raw)):
            profile.append(raw[i]['url'])
    return profile


def user_search(search_queue, token, giant_id_list):
    current_time = time.ctime().split(' ')
    age_queue = search_queue['bdate'] - search_queue['age_limit']
    while age_queue <= (search_queue['bdate'] + search_queue['age_limit'])\
            or (int(current_time[len(current_time)-1]) - age_queue) < 18:
        if search_queue['relation'] == 0:
            relation_list = [1, 2, 3, 4, 5, 6, 7, 8]
        else:
            relation_list = [1, 5, 6]
        for relation in relation_list:
            print(f'Год рождения: {age_queue}; '
                  f'Статус - {ke.relation_id[relation]}')
            params = {
                'q': '',
                'count': 1000,
                'city': search_queue['city'],
                'sex': search_queue['sex'],
                'status': relation,
                'birth_year': age_queue,
                'has_photo': 1,
                'v': 5.99
            }
            response_id = vt.request('https://api.vk.com/method/users.search',
                                     vt.parameters(token, params))
            search_data = response_id['response']['items']
            for user in search_data:
                try:
                    giant_id_list.index(user['id'])
                except ValueError:
                    giant_id_list.append(user['id'])
        age_queue += 1
    return giant_id_list


def partner_list(ban, user_info, id_list, standarts, token):
    potential_partner_list = {}
    progress = 0
    for partner_id in id_list:
        progress += 1
        if str(partner_id) not in ban:
            raw_weight = ud.user_comparison(user_info,
                                            ud.user_interests(partner_id,
                                                              token),
                                            standarts)
            final_weight = 0
            if raw_weight:
                for value in raw_weight.values():
                    if not value:
                        value = 0
                    final_weight = final_weight + value
                potential_partner_list[partner_id] = final_weight
            print(f'{progress} потенциальных партнеров'
                  f' из {len(id_list)} обработано')
    list_sorted = sorted(potential_partner_list.items(),
                         key=lambda x: x[1], reverse=True)
    return list_sorted


def partner_photo(potential_partner_list, token):
    count = 1
    result = []
    if len(potential_partner_list) == 0:
        return None
    if len(potential_partner_list) >= 10:
        count_limit = 10
    else:
        count_limit = len(potential_partner_list)
    for partner_id in potential_partner_list:
        if count <= count_limit:
            temp_dict = {'id': partner_id[0],
                         'photo': profile_pictures(partner_id[0], token),
                         'url': f'https://vk.com/id{partner_id[0]}'}
            if temp_dict['photo'] is not None:
                count += 1
                result.append(temp_dict)
    return result
