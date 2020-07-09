import requests
import json
import time

search_list_keys = ['activities', 'books', 'city', 'faculty_name', 'games', 'home_town', 'interests', 'movies',
                    'music', 'occupation', 'religion', 'religion_2', 'tv']
relation_id = {'1': 'не женат/не замужем', '2': 'есть друг/подруга', '3': 'помолвлен(а)', '4': 'женат/замужем',
            '5': 'всё сложно', '6': 'в активном поиске', '7': 'влюблен(а)', '8': 'в гражданском браке'}

def profile_pictures(user_id, token):
    response_id = requests.get(
        'https://api.vk.com/method/photos.get',
        params={
            'access_token': token,
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 150,
            'v': 5.99
        }
    )
    print(f'Обрабатывается профиль пользователя id{user_id}')
    time.sleep(1)
    try:
        photo_data = response_id.json()['response']['items']
    except KeyError:
        return None
    raw = []
    for profile_picture in photo_data:
        temp_dictionary = {'like': profile_picture['likes']['count'], 'date': profile_picture['date']}
        for size in profile_picture['sizes']:
            if size['type'] == 'x':
                temp_dictionary['url'] = size['url']
                break
        raw.append(temp_dictionary)
    raw.sort(reverse = True, key = lambda x: (x['like'], x['date']))
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
    age_queue = search_queue['bdate'] - search_queue['age_limit']
    while age_queue <= (search_queue['bdate'] + search_queue['age_limit']) or (2020 - age_queue) < 18:
        if search_queue['relation'] == 0:
            relation_list = [1, 2, 3, 4, 5, 6, 7, 8]
        else:
            relation_list = [1, 5, 6]
        for relation in relation_list:
            print(f'Год рождения: {age_queue}; Статус - {relation_id[str(relation)]}')
            response_id = requests.get(
                'https://api.vk.com/method/users.search',
                params={
                    'access_token': token,
                    'q': '',
                    'count': 1000,
                    'city': search_queue['city'],
                    'sex': search_queue['sex'],
                    'status': relation,
                    'birth_year': age_queue,
                    'has_photo': 1,
                    'v': 5.99
                }
            )

            search_data = response_id.json()['response']['items']
            time.sleep(1)
            for user in search_data:
                try:
                    giant_id_list.index(user['id'])
                except ValueError:
                    giant_id_list.append(user['id'])
        age_queue += 1
    return giant_id_list

def partner_photo(potential_partner_list, token):
    count = 1
    result = []
    for partner_id in potential_partner_list:
        if count <= 10:
            temp_dict = {}
            temp_dict['id'] = partner_id[0]
            temp_dict['photo'] = profile_pictures(partner_id[0], token)
            if temp_dict['photo'] is not None:
                count += 1
                result.append(temp_dict)
    return result