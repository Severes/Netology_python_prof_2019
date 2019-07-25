import requests
import psycopg2
import re
import json
import datetime
from time import sleep
from urllib.parse import urlencode
from pprint import pprint

# TODO: Что делаем
#  1. Делаем класс - пользователь
#  2. Собираем критерии из аккаунта пользователя:
#   Возраст
#   Пол
#   Группы
#   Расположение - город
#   Интересы
#   Доп. критерий - отношение к курению
#  3. Проставить вес критериев из шага 2
#  4. Разбирать критерий "Интересы" неоходимо регулярным выражением
#  5. Возвращаем id пользователей, подошедших под условия вместе с тремя фотографиями аватара

# TODO: Требования к программе:
#  1. Нужно получать токен с правами пользователя
#  2. Декомпозиция
#  3. Результат, то есть соответствие пользователей заисывать в БД
#  4. Не должно быть повторений при повторном поиске
#  5. Реализовать тесты на первые запросы. - УТОЧНИТЬ


# Запрос токена
def get_access_token(user_id):
    """
    Запрашивает токен упользователяпо его id vk или псевдониму
    :return: ссылка для авторизации пользователя
    """
    oauth_url = 'https://oauth.vk.com/authorize'
    app_id = 6849372
    auth_data = {
        'client_id': app_id,
        'redirect_uti': 'www.ok.ru',
        'display': 'page',
        'scope': 'status, friends, users, photos, offline',
        'response_type': 'token',
        'v': 5.101
    }
    result = print('?'.join((oauth_url, urlencode(auth_data))))
    return result

# TOKEN
token = '7f4c79e6f0116ddb437929100ac36076f91b6a5bab3daa5a01ddea01efa3bc11527c22ed9afde8861f54a'


class User:

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        """
        :return: Возвращает ссылку на профиль Вконтакте пользователя, чей ID указан при вызове
        текущего класса
        """
        params = self.get_params()
        params['user_ids'] = self.user_id
        params['fields'] = 'domain'
        response_users_get = requests.get('https://api.vk.com/method/users.get', params)
        result_users_get = response_users_get.json()['response'][0]['domain']
        link = 'https://vk.com/' + result_users_get
        return link

    def get_params(self):
        return {
            'access_token': token,
            'v': 5.101
        }

    def regex_interests(self, text):
        """
        Разбирает  весь текст на отдельные слова и складывает в множество
        :return: Множество
        """
        pattern = '[\w]+'
        text = re.findall(pattern, text, re.U)
        return text

    def get_group_list(self):
        """
        :param ids: Имя пользователя Вконтакте или его id
        :return: Список ID всех групп пользователя
        """
        params = self.get_params()
        params['user_id'] = self.user_id
        response_group_list = requests.get('https://api.vk.com/method/groups.get', params)
        result_groups_list = response_group_list.json()['response']['items']
        return result_groups_list

    def check_pair_users_in_groups_search(self, group_list, count=2):
        """
        Проверяет пользователей в группах главного пользователя
        :param group_list: список групп главного пользователя
        :param count: количество групп, в котором должен состоять пользователь-пара, чтобы попасть
        в дальнейшую выборку
        :return: список пользователей-пар
        """
        params = self.get_params()
        users_list = list()
        sorted_user_list = list()
        for group in group_list:
            params['group_id'] = group
            params['count'] = 1000
            while True:
                try:
                    response = requests.get('https://api.vk.com/method/users.search', params)
                    result = response.json()['response']['items']
                    sleep(0.25)
                    # print(result)
                    for item in result:
                        users_list.append(item['id'])
                    # print(len(users_list))
                except requests.exceptions.ReadTimeout:
                    continue
                except KeyError:
                    result_error = response.json()['error']['error_msg']
                    print(result_error)
                    continue
                break
        for elem in users_list:
            if users_list.count(elem) > count:
                if elem not in sorted_user_list:
                    sorted_user_list.append(elem)
        result = sorted_user_list
        return result

    def get_user_parameters(self):
        """
        :return: Возвращает параметры пользователя:
            Пол - sex
            Возраст - bdate
            Группы - нужно зарпашивать через отлельную функцию - get_group_list()
            Расположение - город - city
            Cемейное положение - relation
        """
        user_params_dict = dict()
        params = self.get_params()
        params['user_ids'] = self.user_id
        params['fields'] = 'bdate, sex, city, interests, relation'
        response_users_get = requests.get('https://api.vk.com/method/users.get', params)
        result_users_get = response_users_get.json()['response'][0]
        for key, value in result_users_get.items():
                if key in (params['fields']):
                    if key == 'interests':
                        value = self.regex_interests(value)
                    elif key == 'bdate':
                        key = 'birth_year'
                        value = value.split('.')
                        value = value[2]
                    elif key == 'city':
                        value = value['id']
                    user_params_dict[key] = value
        user_params_dict['group_id'] = self.get_group_list()
        result = user_params_dict
        return result

    def get_pair_user_parameters(self, user_id):
        """
        :return: Возвращает параметр "interests" пользователя-пары:
        """
        user_params_dict = dict()
        params = self.get_params()
        params['user_ids'] = user_id
        params['fields'] = 'interests'
        response_users_get = requests.get('https://api.vk.com/method/users.get', params)
        while True:
            try:
                result_users_get = response_users_get.json()['response'][0]
                sleep(0.3)
                for key, value in result_users_get.items():
                    if key == 'interests':
                        value = self.regex_interests(value)
                        user_params_dict[key] = value
                result = user_params_dict
            except requests.exceptions.ReadTimeout:
                continue
            except KeyError:
                result_error = response_users_get.json()['error']['error_msg']
                print(result_error)
                continue
            break
        return result

    def get_pair_user_lists(self):
        """
        Основная функция
        :return: Возвращает список пользователей с совпадениями по характеристикам основного пользователя
        """
        user_params = self.get_user_parameters()
        user_dict = dict()
        user_interests = user_params.get('interests')
        param = ['sex', 'group_id', 'city', 'birth_year', 'relation']
        del(user_params['interests'])
        pair_user_list = list()
        first_ten_users = list()
        for key, value in user_params.items():
            if key == 'group_id':
                print(key)
                params = self.get_params()
                params['count'] = 1000
                for item in value:
                    params[key] = item
                    while True:
                        try:
                            response = requests.get('https://api.vk.com/method/users.search', params)
                            result = response.json()['response']['items']
                            sleep(0.25)
                            for item in result:
                                if item['id'] in user_dict:
                                    user_dict[item['id']] += key
                                else:
                                    user_dict[item['id']] = key
                            # print(len(user_dict))
                        except requests.exceptions.ReadTimeout:
                            continue
                        except KeyError:
                            result_error = response.json()['error']['error_msg']
                            print(result_error)
                            continue
                        break
            elif key == 'sex':
                params = self.get_params()
                params['count'] = 1000
                print(key)
                if value == 1:
                    params['sex'] = 2
                elif value == 2:
                    params['sex'] = 1
                while True:
                    try:
                        response = requests.get('https://api.vk.com/method/users.search', params)
                        result = response.json()['response']['items']
                        sleep(0.2)
                        for item in result:
                            if item['id'] in user_dict:
                                user_dict[item['id']] += key
                            else:
                                user_dict[item['id']] = key
                        # print(len(user_dict))
                    except requests.exceptions.ReadTimeout:
                        continue
                    except KeyError:
                        result_error = response.json()['error']['error_msg']
                        print(result_error)
                        continue
                    break
            else:
                params = self.get_params()
                params['count'] = 1000
                params[key] = value
                print(key)
                while True:
                    try:
                        response = requests.get('https://api.vk.com/method/users.search', params)
                        result = response.json()['response']['items']
                        sleep(0.2)
                        for item in result:
                            if item['id'] in user_dict:
                                user_dict[item['id']] += key
                            else:
                                user_dict[item['id']] = key
                        # print(len(user_dict))
                    except requests.exceptions.ReadTimeout:
                        continue
                    except KeyError:
                        result_error = response.json()['error']['error_msg']
                        print(result_error)
                        continue
                    break
        # # Часть с проверкой по интересам пользователей
        # for pair_user in pair_user_list:
        #     count = 0
        #     pair_user_interests = self.get_pair_user_parameters(pair_user)
        #     for interest in user_interests:
        #         if interest in pair_user_interests:
        #             count += 1
        #             print('Совпадение!')
        #     if count < 1:
        #         pair_user_list.remove(pair_user)
        # # Часть с проверкой по интересам пользователей
        # Добавляем id тобранных пользователей в список.
        # От веса параметра зависит количество добавений польщователя в список
        for key, value in user_dict.items():
            for p in param:
                if p in value:
                    pair_user_list.append(key)
        pair_user_list = sorted(pair_user_list, key=lambda x: pair_user_list.count(x), reverse=True)
        for user in pair_user_list:
            if len(first_ten_users) < 10:
                if user not in first_ten_users:
                    first_ten_users.append(user)
            else:
                break
        for item in first_ten_users:
            sleep(0.2)
            print(User(item))
        return first_ten_users

    def filter_users_to_get_pairs(self):
        """
        Фильтрует список пользователей через каждый отдельный ОБЩИЙ параметр информации о пользователе:
        В порядке убывания в списке параметров, убывает и вес параметра
        1. Общие группы
        2. Общие интересы
        3. Противоположниый пол (если не задано иное значение)
        4. Одинаковый возраст (если не задано иное значение)
        5. Одинаковый город (если не задано иное значение)
        6. Одинаковое семейное положение (если не задано иное значение)
        :return: итоговый список пользователей, имеющие максимально общие параметры с главным пользователем
        """
        main_user_dict = self.get_user_parameters()
        print('dict', main_user_dict['groups'])
        pair_users_ids = list()
        for key, value in main_user_dict.items():
            print(key)
            if key == 'groups':
                pair_users_ids = self.check_pair_users_in_groups_search(value)
                print(key, pair_users_ids)
            if key == 'interests':
                for elem in value:
                    print(elem)
                    print(value)
                    for user_ids in pair_users_ids:
                        user_interests = self.get_pair_user_parameters(user_ids, key)
                        if value not in user_interests:
                            pair_users_ids.remove(user_ids)
                print(key, pair_users_ids)
            if key in ('sex', 'relation'):
                    for user_ids in pair_users_ids:
                        user_sex_relation = self.get_pair_user_parameters(user_ids, key)
                        if value != user_sex_relation:
                            pair_users_ids.remove(user_ids)
                    print(key, pair_users_ids)
            if key == 'bdate':
                value = value.split('.')
                for user_ids in pair_users_ids:
                    user_bdate = self.get_pair_user_parameters(user_ids, 'birth_year')
                    if value[2] != user_bdate:
                        pair_users_ids.remove(user_ids)
                print('birth_year', pair_users_ids)
            if key == 'city':
                for user_ids in pair_users_ids:
                    user_city = self.get_pair_user_parameters(user_ids, key)
                    if value['id'] != user_city:
                        pair_users_ids.remove(user_ids)
                print(key, pair_users_ids)
        return pair_users_ids

    def filter_users_to_get_pairs_2(self):
        """
        Фильтрует список пользователей через каждый отдельный ОБЩИЙ параметр информации о пользователе:
        В порядке убывания в списке параметров, убывает и вес параметра
        1. Общие группы
        2. Общие интересы
        3. Противоположниый пол (если не задано иное значение)
        4. Одинаковый возраст (если не задано иное значение)
        5. Одинаковый город (если не задано иное значение)
        6. Одинаковое семейное положение (если не задано иное значение)
        :return: итоговый список пользователей, имеющие максимально общие параметры с главным пользователем
        """
        main_user_dict = self.get_user_parameters()
        pair_users_ids = self.check_pair_users_in_groups_search(main_user_dict['groups'], 5)

        sex_list = list()
        print('groups', pair_users_ids)
        print('interests', pair_users_ids)
        for user_ids in pair_users_ids:
            user_sex = self.get_pair_user_parameters(user_ids, 'sex')
            if main_user_dict['sex'] == user_sex or user_sex is None:
                print(main_user_dict['sex'], user_sex)
                print('равен')
                for elem in pair_users_ids:
                    if elem == user_ids:
                        pair_users_ids.remove(user_ids)
            else:
                sex_list.append(user_ids)
                print(main_user_dict['sex'], user_sex)
                print('не равен')
        print(sex_list)
        print('sex', pair_users_ids)
        for user_ids in pair_users_ids:
            user_relation = self.get_pair_user_parameters(user_ids, 'relation')
            if main_user_dict['relation'] != user_relation:
                pair_users_ids.remove(user_ids)
        print('relation', pair_users_ids)
        for user_ids in pair_users_ids:
            user_bdate = self.get_pair_user_parameters(user_ids, 'birth_year')
            if main_user_dict['bdate'][2] != user_bdate:
                pair_users_ids.remove(user_ids)
        print('birth_year', pair_users_ids)
        for user_ids in pair_users_ids:
            user_city = self.get_pair_user_parameters(user_ids, 'city')
            if main_user_dict['city']['id'] != user_city:
                pair_users_ids.remove(user_ids)
        print('city', pair_users_ids)
        return pair_users_ids





# Запрашиваем токен
# get_access_token(80619823)

# 72643786
# 80619823

user = User(80619823)

pprint(User.get_pair_user_lists(user))

# pprint(User.get_pair_user_parameters(user, '80619823, 72643786'))