import requests
from time import sleep, clock, process_time
import datetime
from pprint import pprint
import json

# TODO:
#  1. Получить id пользователя, если на входе было получено имя пользователя Вконтакте
#  2. Получить список групп пользователя
#  3. Получить список друзей пользователя
#  4. Пройтись циклом по каждой группе и сравнить участников группы со списком друзей пользователя.
#  Если в группе отсутствует все друзья пользователя - запишем информацию о группе в итоговый файл groups.json


def get_params():
    return {
        'access_token': '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1',
        'v': 5.92
    }


"""
Все функции автономны. Можно вызывать каждую в отдельности
"""


def get_user_id(nickname_id):
    """
    :param nickname_id: Имя пользователя Вконтакте или его id
    :return: ID пользователя
    """
    params = get_params()
    params['user_ids'] = nickname_id
    response_for_id = requests.get('https://api.vk.com/method/users.get', params)
    result_for_id = response_for_id.json()['response'][0]['id']
    return result_for_id


def get_group_list(ids):
    """
    :param ids: Имя пользователя Вконтакте или его id
    :return: Список ID всех групп пользователя
    """
    id = get_user_id(ids)
    params = get_params()
    params['user_id'] = id
    response_group_list = requests.get('https://api.vk.com/method/groups.get', params)
    result_groups_list = response_group_list.json()['response']['items']
    return result_groups_list


def get_user_friends_list(ids):
    """
    :param ids: Имя пользователя Вконтакте или его id
    :return: Список ID друзей пользователя
    """
    id = get_user_id(ids)
    params = get_params()
    params['user_id'] = id
    response_friends_list = requests.get('https://api.vk.com/method/friends.get', params)
    result_friends_list = response_friends_list.json()['response']['items']
    return result_friends_list


def check_for_friends_in_groups(ids):
    """
    :param ids: Имя пользователя Вконтакте или его id
    :return: Множество групп, в которых нет ни одного друга пользователя
    """
    group_list = get_group_list(ids)
    friend_list = get_user_friends_list(ids)
    result_list_1 = set()
    result_list_0 = set()
    result_list = set()
    count = int()
    for group in group_list:
        for friend in friend_list:
            while True:
                params = get_params()
                params['group_id'] = group
                params['user_id'] = friend
                try:
                    response_friend_in_group = requests.get('https://api.vk.com/method/groups.isMember', params)
                    sleep(0.2)
                    result = response_friend_in_group.json()['response']
                    if result == 1:
                        print('Результат по другу {} в группе {}: {}. Осталось проверить друзей {}'.format(friend, group, result, len(friend_list) * len(group_list) - count))
                        result_list_1.add(group)
                        count += 1
                    elif result == 0:
                        print('Результат по другу {} в группе {}: {}. Осталось проверить друзей {}'.format(friend, group, result, len(friend_list) * len(group_list) - count))
                        result_list_0.add(group)
                        count += 1
                except requests.exceptions.ReadTimeout:
                    continue
                except KeyError:
                    result_error = response_friend_in_group.json()['error']['error_msg']
                    print('Возникла ошибка: ', result_error)
                    continue
                break
        result_list = result_list_0.difference(result_list_1)
    return create_json_file(result_list)


def create_json_file(set_income):
    """
    :param set_income: Множество ID групп
    :return: Файл в формате json c описанием групп из множества
    """
    json_list = list()
    params = get_params()
    params['fields'] = 'members_count'
    for group in set_income:
        while True:
            params['group_id'] = group
            print('Запрос информации по группе № {}'.format(group))
            try:
                response_for_group_info = requests.get('https://api.vk.com/method/groups.getById', params)
                sleep(0.3)
                result_for_group_info = response_for_group_info.json()['response'][0]
                group_dict = dict()
                group_dict['name'] = result_for_group_info['name']
                group_dict['gid'] = result_for_group_info['id']
                group_dict['members_count'] = result_for_group_info['members_count']
                json_list.append(group_dict)
            except requests.exceptions.ReadTimeout:
                continue
            except KeyError:
                result_error = response_for_group_info.json()['error']['error_msg']
                print('Возникла ошибка: ', result_error)
                continue
            break
    with open('groups.json', 'w', encoding='utf-8') as json_text:
        data = json_list
        json.dump(data, json_text, indent=2, ensure_ascii=False)  # сериализация записываемого файла
        some_text = json.dumps(data, indent=2, ensure_ascii=False)
    print('Запрос выполнен успешно! Результат записан в файл "groups.json"')
    return some_text


print(check_for_friends_in_groups('eshmargunov'))
