import requests
import json
import time

search_list_keys = ['activities', 'books', 'city', 'faculty_name', 'games', 'home_town', 'interests', 'movies',
                    'music', 'occupation', 'religion', 'religion_2', 'tv']

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
    photo_data = response_id.json()['response']['items']
    raw = []
    for profile_picture in photo_data:
        temp_dictionary = {'like': profile_picture['likes']['count'], 'date': profile_picture['date']}
        for size in profile_picture['sizes']:
            if size['type'] == 'x':
                temp_dictionary['url'] = size['url']
                break
        raw.append(temp_dictionary)
    raw.sort(reverse = True, key = lambda x: (x['like'], x['date']))
    return raw[:3]


def user_search(search_queue, token, giant_id_list):
    age_queue = search_queue['bdate'] - search_queue['age_limit']
    while age_queue <= (search_queue['bdate'] + search_queue['age_limit']) or (2020 - age_queue) < 18:
        if search_queue['relation'] == 0:
            relation_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            relation_list = [0, 1, 5, 6]
        for relation in relation_list:
            print(f'{age_queue} - {relation}')
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
            print(search_data)
            time.sleep(1)
            for user in search_data:
                try:
                    giant_id_list.index(user['id'])
                except ValueError:
                    giant_id_list.append(user['id'])
        age_queue += 1
    return giant_id_list
