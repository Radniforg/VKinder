import requests
import re
import time
import settings as se
import keyholder as ke
import vk_token as vt
import sys

def user_profile(token, username):
    previous_token = token
    current_token = vt.token_confirmation(se.app_id, previous_token)
    user = vt.user_confirmed(username, current_token)
    if not user:
        sys.exit()
    user_info = user_interests(user, current_token)
    user_info['bdate'] = birthday(user_info)
    return user_info


def user_interests(user_id, token):
    elements = {}
    response_id = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': token,
            'user_ids': user_id,
            'fields': 'sex, bdate, city, home_town, education, occupation,'
                      ' relation, connections, activities, interests, music,'
                      ' movies, tv, books, games, is_friend, religion,'
                      ' personal, common_count',
            'v': 5.103
        }
    )
    time.sleep(1)
    combined_data = response_id.json()['response'][0]
    for key in ke.basic_interest_keys:
        elements[key] = combined_data.get(key)
    for key in ke.small_list_keys:
        if combined_data.get(key):
            elements[key] = combined_data.get(key).replace('\t', ', ').split(', ')
            for i in range(len(elements[key])):
                elements[key][i] = elements[key][i].lower()
        else:
            elements[key] = combined_data.get(key)
    temp_element = combined_data.get('personal')
    if type(temp_element) is dict:
        elements['religion'] = [combined_data.get('religion'),
                                temp_element.get('religion')]
        for key in ke.personal_interest_keys:
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
    standart_matrix = se.standart_matrix
    user_matrix = {}
    correct_input = False
    while not correct_input:
        user_input = input('Введите допустимую для вас разницу'
                           ' в возрасте:\n')
        try:
            standart_matrix['age_limit'] = int(user_input)
            correct_input = True
        except ValueError:
            print('Некорректный ввод')
    correct_input = False
    while not correct_input:
        user_love_interest = input('Если вы ищете любовный интерес '
                                   '- нажмите Д. Если вы ищете '
                                   'собеседника - нажмите Н\n')
        if user_love_interest.lower() == 'н':
            correct_input = True
        elif user_love_interest.lower() == 'д':
            standart_matrix['relation_ban'] = 1
            while not correct_input:
                user_preferences = input('Пожалуйста, укажите '
                                         'желаемый пол партера: '
                                         'М/Ж/Л(любой):\n')
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
        user_response = input('Если хотите самостоятельно настроить '
                              'важность параметров партнера, '
                              'нажмите Д. Для продолжения со '
                              'стандартными параметрами нажмите Н\n')
        if user_response.lower() == 'н':
            for key in standart_matrix.keys():
                user_matrix[key] = standart_matrix[key]
            correct_input = True
        elif user_response.lower() == 'д':
            for key in standart_matrix.keys():
                if key == 'relation_ban' or key == 'sex_preference' \
                        or key == 'age_limit':
                    user_matrix[key] = standart_matrix[key]
                else:
                    inter_correct_input = False
                    while not inter_correct_input:
                        user_input = input(f'Пожалуйста, введите значимость '
                                           f'параметра {key}'
                                           f' ({se.translator[key]})'
                                           f' по шкале от 0 до 9 '
                                           f'(целое число):\n')
                        if re.match('^\d$', user_input):
                            user_matrix[key] = int(user_input)
                            inter_correct_input = True
                        else:
                            print('Ошибка, некорректный ввод!')
            correct_input = True
        else:
            print('Некорректная команда. Повторите ввод')
    return user_matrix

def bad_habits(user_elements, partner_elements, standart_matrix):
    # Проверяет совместимость по отношению к курению
    if user_elements['smoking'] not in [0, 3, 4, None] \
            and standart_matrix['smoking'] > 0:
        if abs(user_elements['smoking'] - partner_elements['smoking']) > 2 \
                and partner_elements['smoking'] != 4:
            return None
    # Проверяет совместимость по отношению к алкоголю
    if user_elements['alcohol'] not in [0, 3, 4, None] \
            and standart_matrix['alcohol'] > 0:
        if abs(user_elements['alcohol'] - partner_elements['alcohol']) > 2 \
                and partner_elements['alcohol'] != 4:
            return None
    return 1

def ages(user_elements, partner_elements, standart_matrix):
    try:
        user_bdate = int(user_elements['bdate'].split('.')[2])
        partner_bdate = int(partner_elements['bdate'].split('.')[2])
        age_weight = (int(standart_matrix['age_limit']) -
                                    abs(user_bdate - partner_bdate) + 0.1)\
                                   * standart_matrix['age_difference']
        return age_weight
    except IndexError:
        return 0
    except AttributeError:
        return 0

def user_comparison(user_elements, partner_elements, standart_matrix):
    if not bad_habits(user_elements, partner_elements, standart_matrix):
        return None
    raw_data_weight = {'bdate': ages(user_elements, partner_elements, standart_matrix),
                       'common_count': partner_elements['common_count'] / \
                                      (10 - standart_matrix['common_count'])}
    # данные, сравнивающие интересы, книги и тд
    for key in ke.small_list_keys:
        raw_data_weight[key] = 0
        if type(partner_elements[key]) is list \
                and type(user_elements[key]) is list:
            for partner_interest in partner_elements[key]:
                if partner_interest in user_elements[key]:
                    raw_data_weight[key] += standart_matrix[key]
    # Сравнение простых параметров (город, место рождения, религия и т.д.
    for key in ke.basic_list_keys:
        raw_data_weight[key] = 0
        if user_elements[key] and key != 'common_count':
            if user_elements.get(key) == partner_elements.get(key)\
                    and user_elements.get(key):
                raw_data_weight[key] = standart_matrix[key]
    return raw_data_weight

def birthday(user_information):
    try:
        year = int(user_information['bdate'].split('.')[2])
        return user_information['bdate']
    except (IndexError, AttributeError):
        correct_input = False
        while not correct_input:
            year = input('Пожалуйста, укажите ваш год рождения: \n')
            bdate = f'..{year}'
            try:
                user_information['bdate'] = int(bdate.split('.')[2])
                return bdate
            except ValueError:
                print('Некорректный ввод!')



if __name__ == '__main__':
    pass