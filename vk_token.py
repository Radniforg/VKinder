import requests
from urllib.parse import urlencode
import time
import os


def settings_save(filepath, set_name, set_value):
    with open(filepath, 'r') as settings:
        file_lines = settings.readlines()
        for line in file_lines:
            if set_name in line:
                index = file_lines.index(line)
                line = line.rstrip()
                setting_swap = line.split('"')
                new_line = setting_swap[0] + '"' + set_value + '"\n'
                line = line.replace(line, new_line)
                file_lines[index] = line
    with open(filepath, 'w') as settings:
        for line in file_lines:
            settings.write(line)
            settings.flush()
            os.fsync(settings)
    return None


def parameters(token, add_params: dict = None):
    params = {
        'access_token': token
    }
    if add_params and type(add_params) is dict:
        for key, value in add_params.items():
            params[key] = value
    return params


def request(url, params):
    response = requests.get(url, params)
    time.sleep(1)
    return response.json()


def token_confirmation(app_id, token='', filepath='settings.py'):
    # Проверка работоспособности токена
    check_bool = False
    while not check_bool:
        token_check = request('https://api.vk.com/method/users.get',
                              parameters(token, {'v': 5.103}))
        try:
            token = token_check['error']
            OAUTH_URL = 'https://oauth.vk.com/authorize'
            OAUTH_PARAMS = {
                'client_id': app_id,
                'display': 'page',
                'scope': 'groups,friends',
                'response_type': 'token',
                'v': 5.52
            }
            print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))
            full_url = input('Пожалуйста, пройдите по ссылке и'
                             ' скопируйте полностью полученный URL:\n')
            half_token = full_url.split('=')[1]
            token = half_token.split('&')[0]
            print(f'Token - {token}')
        except KeyError:
            check_bool = True
    settings_save(filepath, 'token', token)
    return token


def user_confirmed(user1, token, filepath='settings.py'):
    # Получение id пользователя
    username_confirmation = False
    if user1 == '':
        user1 = input('Пожалуйста, введите id пользователя: \n')
    while not username_confirmation:
        response_id = request('https://api.vk.com/method/users.get',
                              parameters(token, {'user_ids': user1,
                                                 'v': 5.103}))
        try:
            user_id = response_id['response'][0]['id']
            username_confirmation = True
        except KeyError:
            print(response_id)
            correct_input = False
            while not correct_input:
                function_suspension = input('Некорректное имя пользователя. '
                                            'Хотите продолжить (Y/N):\n')
                if function_suspension.lower() == 'n':
                    return None
                elif function_suspension.lower() == 'y':
                    user1 = input('Пожалуйста, введите имя пользователя'
                                  ' или его id:\n')
                    correct_input = True
                else:
                    print('Некорректная команда. Повторите ввод')
        except IndexError:
            print(response_id)
            correct_input = False
            while not correct_input:
                function_suspension = input('Некорректное имя пользователя. '
                                            'Хотите продолжить (Y/N):\n')
                if function_suspension.lower() == 'n':
                    return None
                elif function_suspension.lower() == 'y':
                    user1 = input('Пожалуйста, введите имя пользователя'
                                  ' или его id:\n')
                    correct_input = True
                else:
                    print('Некорректная команда. Повторите ввод')
    settings_save(filepath, 'user_id', str(user_id))
    return user_id
