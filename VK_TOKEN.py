import requests
from urllib.parse import urlencode

def token_confirmation(app_id, TOKEN = ''):
    #Проверка работоспособности токена
    token = TOKEN
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
            token = input('Пожалуйста, пройдите по ссылке и'
                          ' вставьте корректный TOKEN:\n')
        except KeyError:
            check_bool = True
    return token


def user_confirmed(user1, TOKEN):
    # Получение id пользователя
    username_confirmation = False
    while not username_confirmation:
        response_id = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': TOKEN,
                'user_ids': user1,
                'v': 5.103
            }
        )
        try:
            user_id = response_id.json()['response'][0]['id']
            username_confirmation = True
        except KeyError:
            correct_input = False
            while not correct_input:
                function_suspension = input('Некорректное имя пользователя. '
                                            'Хотите продолжить (Y/N):\n')
                if function_suspension.lower() == 'n':
                    return 'Программа остановлена пользователем. ' \
                           'Некорректное имя пользователя'
                elif function_suspension.lower() == 'y':
                    user1 = input('Пожалуйста, введите имя пользователя'
                                  ' или его id:\n')
                    correct_input = True
                else:
                    print('Некорректная команда. Повторите ввод')
    return user_id