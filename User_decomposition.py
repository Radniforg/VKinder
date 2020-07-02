import requests
import json
import re

def user_interests(user_id, token):
    elements = {}
    response_id = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': token,
            'user_ids': user_id,
            'fields': 'sex, bdate, city, home_town, education, occupation, relation,'
                      ' connections, activities, interests, music, movies, tv, books,'
                      ' games, is_friend, religion, personal, common_count, follower_count',
            'v': 5.103
        }
    )
    combined_data = response_id.json()['response'][0]
    elements['bdate'] = combined_data.get('bdate')
    elements['city'] = combined_data.get('city')['id']
    elements['faculty_name'] = combined_data.get('faculty_name')
    elements['is_friend'] = combined_data.get('is_friend')
    elements['occupation'] = combined_data.get('occupation')['name']
    elements['relation'] = combined_data.get('relation')
    elements['sex'] = combined_data['sex']
    elements['activities'] = combined_data.get('activities')
    elements['books'] = combined_data.get('books').replace('\t',', ').split(', ')
    elements['games'] = combined_data.get('games').replace('\t',', ').split(', ')
    elements['home_town'] = combined_data.get('home_town')
    elements['interests'] = combined_data.get('interests').replace('\t',', ').split(', ')
    elements['movies'] = combined_data.get('movies').replace('\t',', ').split(', ')
    elements['music'] = combined_data.get('music').replace('\t',', ').split(', ')
    elements['tv'] = combined_data.get('tv').replace('\t',', ').split(', ')
    elements['religion'] = combined_data.get('religion')
    elements['common_count'] = combined_data.get('common_count')
    elements['follower_count'] = combined_data.get('follower_count')
    temp_element = combined_data.get('personal')
    elements['political'] = temp_element.get('political')
    elements['religion_2'] = temp_element.get('religion')
    elements['people_main'] = temp_element.get('people_main')
    elements['life_main'] = temp_element.get('life_main')
    elements['smoking'] = temp_element.get('smoking')
    elements['alcohol'] = temp_element.get('alcohol')
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
        'follower_count': 0,
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
        'religion_2': 0,
        'smoking': 0,
        'tv': 0
    }
    user_matrix = {}
    correct_input = False
    while not correct_input:
        user_love_interest = input(
            'Если вы ищете любовный интерес - нажмите Y. Если вы ищете собеседника - нажмите N\n')
        if user_love_interest.lower() == 'n':
            correct_input = True
        elif user_love_interest.lower() == 'y':
            standart_matrix['relation_ban'] = 1
            while not correct_input:
                user_preferences = input('Пожалуйста, укажите желаемый пол партера: М/Ж/Л(любой):')
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
        user_response = input('Если хотите самостоятельно настроить важность параметров партнера, нажмите Y.'
                              'Для продолжения со стандартными параметрами нажмите N\n')
        if user_response.lower() == 'n':
            user_matrix = standart_matrix
            correct_input = True
        elif user_response.lower() == 'y':
            for key in standart_matrix.keys():
                if key == 'relation_ban' or key == 'sex_preference':
                    user_matrix[key] = standart_matrix[key]
                elif key == 'religion_2':
                    user_matrix[key] = user_matrix['religion']
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


