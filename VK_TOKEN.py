import requests
from urllib.parse import urlencode
import time


def token_confirmation(app_id, token=''):
    # Проверка работоспособности токена
    check_bool = False
    while not check_bool:
        token_check = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': token,
                'v': 5.103
            }
        )
        try:
            token = token_check.json()['error']
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
    return token


def user_confirmed(user1, token):
    # Получение id пользователя
    username_confirmation = False
    if user1 == '':
        user1 = input('Пожалуйста, введите id пользователя: \n')
    while not username_confirmation:
        response_id = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': token,
                'user_ids': user1,
                'v': 5.103
            }
        )
        time.sleep(1)
        try:
            user_id = response_id.json()['response'][0]['id']
            username_confirmation = True
        except KeyError:
            print(response_id.json())
            correct_input = False
            while not correct_input:
                function_suspension = input('Некорректное имя пользователя. '
                                            'Хотите продолжить (Y/N):\n')
                if function_suspension.lower() == 'n':
                    print('Программа остановлена пользователем. '
                          'Некорректное имя пользователя')
                    errorcode = 'ErrorThatCouldNotBeId'
                    return errorcode
                elif function_suspension.lower() == 'y':
                    user1 = input('Пожалуйста, введите имя пользователя'
                                  ' или его id:\n')
                    correct_input = True
                else:
                    print('Некорректная команда. Повторите ввод')
        except IndexError:
            print(response_id.json())
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
    return user_id


def token_settings_save(filepath, token):
    with open(filepath, 'r') as settings:
        file_lines = settings.readlines()
        for line in file_lines:
            if 'token' in line:
                index = file_lines.index(line)
                line = line.rstrip()
                token_swap = line.split('"')
                new_line = token_swap[0] + '"' + token + '"\n'
                line = line.replace(line, new_line)
                file_lines[index] = line
    with open(filepath, 'w') as settings:
        for line in file_lines:
            settings.write(line)
    return None