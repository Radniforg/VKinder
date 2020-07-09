import requests
import json
import re
import time

search_list_keys = ['activities', 'books', 'city', 'faculty_name', 'games', 'home_town', 'interests', 'movies',
                    'music', 'occupation', 'religion', 'tv']
small_list_keys = ['books', 'interests', 'movies', 'music', 'tv', 'games']
basic_list_keys = ['activities', 'city', 'faculty_name', 'home_town', 'religion', 'occupation', 'life_main',
                   'political', 'people_main']
basic_interest_keys = ['bdate', 'faculty_name', 'relation', 'sex', 'activities', 'home_town', 'religion',
                      'common_count']
personal_interest_keys = ['political', 'people_main', 'life_main', 'smoking', 'alcohol']
#special_interest_keys = ['city', 'occupation', 'religion', 'personal']

def user_interests(user_id, token):
    elements = {}
    response_id = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': token,
            'user_ids': user_id,
            'fields': 'sex, bdate, city, home_town, education, occupation, relation,'
                      ' connections, activities, interests, music, movies, tv, books,'
                      ' games, is_friend, religion, personal, common_count',
            'v': 5.103
        }
    )
    time.sleep(1)
    combined_data = response_id.json()['response'][0]
    for key in basic_interest_keys:
        elements[key] = combined_data.get(key)
    for key in small_list_keys:
        if combined_data.get(key):
            elements[key] = combined_data.get(key).replace('\t',', ').split(', ')
            for i in range(len(elements[key])):
                elements[key][i] = elements[key][i].lower()
        else:
            elements[key] = combined_data.get(key)
    temp_element = combined_data.get('personal')
    if type(temp_element) is dict:
        elements['religion'] = [combined_data.get('religion'), temp_element.get('religion')]
        for key in personal_interest_keys:
            elements[key] = temp_element.get(key)
    else:
        elements['religion'] = [combined_data.get('religion'), ]
    for i in range(len(elements['religion'])):
        if elements['religion'][i]:
            elements['religion'][i] = elements['religion'][i].lower()
    temp = combined_data.get('city')
    if temp:
        elements['city'] = temp.get('id')
    else:
        elements['city'] = None
    temp = combined_data.get('occupation')
    if temp:
        elements['occupation'] = temp.get('name').lower()
    else:
        elements['occupation'] = None
    return elements

def user_element_weight():
    #rus = {} - словарь для русификации параметров поиска (для пользовательского ввода)
    standart_matrix = {
        'age_difference': 0,
        'sex_preference': 0,
        'activities': 0,
        'books': 0,
        'city': 0,
        'common_count': 0,
        'faculty_name': 0,
        'games': 0,
        'home_town': 0,
        'interests': 0,
        'life_main': 0,
        'movies': 0,
        'music': 0,
        'occupation': 0,
        'people_main': 0,
        'political': 0,
        'relation_ban': 0,
        'religion': 0,
        'tv': 0,
        'alcohol': 0,
        'smoking': 0
    }
    user_matrix = {}
    correct_input = False
    while not correct_input:
        user_input = input('Введите допустимую для вас разницу в возрасте:\n')
        try:
            standart_matrix['age_limit'] = int(user_input)
            correct_input = True
        except ValueError:
            print('Некорректный ввод')
    correct_input = False
    while not correct_input:
        user_love_interest = input(
            'Если вы ищете любовный интерес - нажмите Д. Если вы ищете собеседника - нажмите Н\n')
        if user_love_interest.lower() == 'н':
            correct_input = True
        elif user_love_interest.lower() == 'д':
            standart_matrix['relation_ban'] = 1
            while not correct_input:
                user_preferences = input('Пожалуйста, укажите желаемый пол партера: М/Ж/Л(любой):\n')
                if user_preferences.lower() == 'м':
                    standart_matrix['sex_preference'] = 2
                    correct_input = True
                elif user_preferences.lower() == 'ж':
                    standart_matrix['sex_preference'] = 1
                    correct_input = True
                elif user_preferences.lower() == 'л':
                    correct_input = True
                else:
                    print('Некорректный ввод')
        else:
            print('Некорректный ввод')
    correct_input = False
    while not correct_input:
        user_response = input('Если хотите самостоятельно настроить важность параметров партнера, нажмите Д.'
                              'Для продолжения со стандартными параметрами нажмите Н\n')
        if user_response.lower() == 'н':
            user_matrix = standart_matrix
            correct_input = True
        elif user_response.lower() == 'д':
            for key in standart_matrix.keys():
                if key == 'relation_ban' or key == 'sex_preference':
                    user_matrix[key] = standart_matrix[key]
                else:
                    inter_correct_input = False
                    while not inter_correct_input:
                        user_input = input(f'Пожалуйста, введите значимость параметра {key} '
                                           f'по шкале от 0 до 9 (целое число):\n')
                        if re.match('^\d$', user_input):
                            user_matrix[key] = user_input
                            inter_correct_input = True
                        else:
                            print('Ошибка, некорректный ввод!')
            correct_input = True
        else:
            print('Некорректная команда. Повторите ввод')
    return user_matrix


def user_comparison(user_elements, partner_elements, standart_matrix):
    # #Проверяет совместимость по отношениям
    # if standart_matrix['relation_ban'] == 1:
    #     if partner_elements['relation'] in [2, 3, 4, 7, 8]:
    #         return None
    # #Проверяет совместимость по полу
    # if standart_matrix['sex_preference'] > 0:
    #     if standart_matrix['sex_preference'] != partner_elements['sex']:
    #         return None
    #Проверяет совместимость по отношению к курению
    if user_elements['smoking'] not in [0, 3, 4, None] and standart_matrix['smoking'] > 0:
        if abs(user_elements['smoking'] - partner_elements['smoking']) > 2 and partner_elements['smoking'] != 4:
            return None
    #Проверяет совместимость по отношению к алкоголю
    if user_elements['alcohol'] not in [0, 3, 4, None] and standart_matrix['alcohol'] > 0:
        if abs(user_elements['alcohol'] - partner_elements['alcohol']) > 2 and partner_elements['alcohol'] != 4:
            return None
    #Сырые данные соотношения с текущим партнером
    raw_data_weight = {}
    #Данные соотношения возрастов
    try:
        raw_data_weight['bdate'] = abs(int(user_elements['bdate'].split('.')[2])
                                       - int(partner_elements['bdate'].split('.')[2]))
    except IndexError:
        raw_data_weight['bdate'] = 100
    except AttributeError:
        return None
    #данные по общим друзьям
    raw_data_weight['common_count'] = partner_elements['common_count']/standart_matrix['common_count']
    #данные, сравнивающие интересы, книги и тд
    for key in small_list_keys:
        raw_data_weight[key] = 0
        if type(partner_elements[key]) is list and type(user_elements[key]) is list:
            for partner_interest in partner_elements[key]:
                if partner_interest in user_elements[key]:
                    raw_data_weight[key] += 1
                if key == 'books':
                    print(f'{partner_interest} - {user_elements[key]}')
    #Сравнение простых параметров (город, место рождения, религия и т.д.
    for key in basic_list_keys:
        raw_data_weight[key] = 0
        if user_elements[key] and key != 'common_count':
            if user_elements.get(key) == partner_elements.get(key) and user_elements.get(key):
                raw_data_weight[key] = 1
    print(raw_data_weight)
    return raw_data_weight



