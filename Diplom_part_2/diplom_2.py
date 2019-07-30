import requests
import re
import datetime
import psycopg2 as pg
from time import sleep
from urllib.parse import urlencode
from pprint import pprint
from operator import itemgetter
import json

# TODO: Остановился на функции get_3_profile_photos.
#       Нужно сформировать json с тремя фотками.
#       Отфильтровать фотки по количеству лайков

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

# Работа с БД
def create_db():
    """
    Создает таблицу, если ее еще нет в БД
    """
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            create table if not exists profile (
                id serial primary key,
                profile_id integer not null
            ) 
             """)
            print('База данных и таблицы созданы')

def pg_db_connect(option,users_list=None):
    """
    :param option: Режим вызова функции.
        insert - вставка значений в БД
        check - проверка наличия значенияв БД
    :param users_list: Список пользователей для проверки/вставки
    :return: возвращает список пользователей из БД
    """
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        if option == 'insert':
            with conn.cursor() as cur:
                for user in users_list:
                    cur.execute("""
                    insert into profile (profile_id) values (%s)
                    """, (user,))
        elif option == 'check':
            with conn.cursor() as cur:
                cur.execute("""
                select profile_id from profile;
                """)
                result = cur.fetchall()
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
        while True:
            try:
                response_users_get = requests.get('https://api.vk.com/method/users.get', params)
                result_users_get = response_users_get.json()['response'][0]['domain']
                sleep(0.25)
                link = 'https://vk.com/' + result_users_get
                return link
            except requests.exceptions.ReadTimeout:
                continue
            except KeyError:
                result_error = response_users_get.json()['error']['error_msg']
                print(result_error)
                continue

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
            Группы - group_id. Нужно зарпашивать через отлельную функцию - get_group_list()
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

    def get_3_profile_photos(self, profile_list):
        """
        Собирает 3 топовых фотографии по списку пользователей и выдает итоговый JSON
        :param profile_list: Список пользователей
        :return: JSON с ссылкой напрофиль и 3 топ фото
        """
        profile_photo_list = list()
        final_profile_list = list()
        params = self.get_params()
        params['album_id'] = 'profile'
        params['extended'] = 1
        for profile in profile_list:
            while True:
                try:
                    print(f'Сбор фотографий по пользователю {User(profile)}')
                    final_profile_dict = dict()
                    params['owner_id'] = profile
                    response_profile_photos = requests.get('https://api.vk.com/method/photos.get', params)
                    result = response_profile_photos.json()['response']['items']
                    for item in result:
                        profile_dict = dict()
                        profile_dict['profile_id'] = item['owner_id']
                        profile_dict['photo'] = item['sizes'][-1]['url']
                        profile_dict['likes'] = item['likes']['count']
                        profile_photo_list.append(profile_dict)
                        profile_photo_list = sorted(profile_photo_list, key=itemgetter('likes'), reverse=True)
                    final_profile_dict['id'] = str((User(profile)))
                    final_profile_dict['photo_1'] = profile_photo_list[0]['photo']
                    final_profile_dict['photo_2'] = profile_photo_list[1]['photo']
                    final_profile_dict['photo_3'] = profile_photo_list[2]['photo']
                    final_profile_list.append(final_profile_dict)
                except KeyError:
                    result_error = response_profile_photos.json()['error']['error_msg']
                    print(result_error)
                    continue
                break
        json_text = print(json.dumps(final_profile_list, indent=2, ensure_ascii=False))
        return json_text

    def get_pair_user_lists(self):
        """
        Основная функция
        :return: Возвращает список пользователей с совпадениями по характеристикам основного пользователя
        """
        # Получаю список параметров пользователя, чтобы по ним искать профили-пар
        user_params = self.get_user_parameters()
        user_dict = dict()
        user_interests = user_params.get('interests')
        param = ['sex', 'group_id', 'city', 'birth_year', 'relation']
        # Удаляю из списка параметров главного пользователя интересы, потому что не знаю, как по ним итерироваться
        del(user_params['interests'])
        pair_user_list = list()
        first_ten_users = list()
        print('Поиск пользователей по параметрам:')
        for key, value in user_params.items():
            if key == 'group_id':
                print('Группы')
                params = self.get_params()
                params['count'] = 1000
                for item in value[:2]:
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
                print('Пол')
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
                if key == 'relation':
                    print('Семейное положение')
                elif key == 'birth_year':
                    print('Год рождения')
                elif key =='city':
                    print('Город')
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
        for key, value in user_dict.items():
            for p in param:
                if p in value:
                    pair_user_list.append(key)
        pair_user_list = sorted(pair_user_list, key=lambda x: pair_user_list.count(x), reverse=True)
        # Создаем таблицу для профилей
        create_db()
        print('Проверяем наличие профилей в базе данных')
        # Формируем список из 10 уникальных профилей
        for user in pair_user_list:
            # проверяем наличие профиля в базе
            if (user,) in pg_db_connect('check'):
                continue
            # если список еще не больше 10, то добавляем его в список уникальных
            if len(first_ten_users) < 10:
                if user not in first_ten_users:
                    first_ten_users.append(user)
            else:
                break
        # Выводим значений отобранных профилей
        print('Количество совпадений параметров с главным профилем поользователя:')
        for item in first_ten_users:
            print(f'{User(item)}. Количество совпадений - {pair_user_list.count(item)}. id - {item}')
        # Добавляем 10 отобранных профилей в базу данных
        pg_db_connect('insert', first_ten_users)
        # print(f'10 пользаков {first_ten_users[:1]}')
        next_func = self.get_3_profile_photos(first_ten_users)
        return next_func


        #
        # with open('profile_list.json', 'w', encoding='utf-8') as json_text:
        #     data = profile_photo_list[:3]
        #     json.dump(data, json_text, indent=2, ensure_ascii=False)
        #     some_text = json.dumps(data, indent=2, ensure_ascii=False)
        # return some_text
        # return  pprint(json_list)


# Запрашиваем токен
# get_access_token(80619823)

# 72643786
# 80619823

user = User(80619823)

pprint(User.get_pair_user_lists(user))

# pprint(User.get_pair_user_parameters(user, '80619823, 72643786'))
# User.get_3_profile_photos(user, [80619823])