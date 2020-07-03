import requests
import json


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