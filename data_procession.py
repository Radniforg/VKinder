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
        temp_dictionary = {}
        temp_dictionary['like'] = profile_picture['likes']['count']
        temp_dictionary['date'] = profile_picture['date']
        for size in profile_picture['sizes']:
            if size['type'] == 'x':
                temp_dictionary['url'] = size['url']
                break
        raw.append(temp_dictionary)
    raw.sort(reverse = True, key = lambda x: (x['like'], x['date']))
    return raw[:5]

def search_hint(token):
    response_id = requests.get(
        'https://api.vk.com/method/search.getHints',
        params={
            'access_token': token,
            'q': 'Tokio',
            'limit': 9,
            'search_global': 1,
            'v': 5.99
        }
    )
    search_data = response_id.json()
    return search_data

def user_search(search_queue, token):
    giant_id_list = []
    if type(search_queue) is not list:
        temp_list = [search_queue]
        search_queue = temp_list
    for current_search in search_queue:
        print(current_search)
        response_id = requests.get(
            'https://api.vk.com/method/users.search',
            params={
                'access_token': token,
                'q': current_search,
                'v': 5.99
            }
        )
        search_data = response_id.json()['response']['items']
        time.sleep(1)
        id_list = []
        for user in search_data:
            try:
                giant_id_list.index(user['id'])
            except ValueError:
                giant_id_list.append(user['id'])
    return giant_id_list

def data_preparation(elements):
    #elements - выходные данные user_interests (user_decomposition.py)
    total_search_values = []
    for key, element in elements.items():
        if key in search_list_keys:
            if type(element) is list:
                for subelement in element:
                    total_search_values.append(subelement)
            else:
                if element:
                    total_search_values.append(element)
    return total_search_values