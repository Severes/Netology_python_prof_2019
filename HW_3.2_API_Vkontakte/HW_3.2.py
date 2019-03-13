import requests
from urllib.parse import urlencode
from pprint import pprint


OAUTH_URL = 'https://oauth.vk.com/authorize'
APP_ID = 6849372

auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'status, friends, users',
    'response_type': 'token',
    'v': 5.92
}

# print('?'.join((OAUTH_URL, urlencode(auth_data))))

"""
Задача №1
Пользователя нужно описать с помощью класса и реализовать метод поиска общих друзей, используя API VK.
Задача №2
Поиск общих друзей должен происходить с помощью оператора &, т.е. user1 & user2 должен 
выдать список общих друзей пользователей user1 и user2, в этом списке должны быть экземпляры классов.
Задача №3
Вывод print(user) должен выводить ссылку на профиль пользователя в сети VK
"""
token = '79f323d4d94c8d87a61d7b35e056fb387ba62f7cfce435e2888570308087864cda417a8b3f6d5e9f44846'


class User:

    def __init__(self, source_uid):
        self.source_uid = source_uid

    def __str__(self):
        """
        :return: Возвращает ссылку на профиль Вконтакте пользователя, чей ID указан при вызове
        текущего класса
        """
        params = self.get_params()
        params['user_ids'] = self.source_uid
        params['fields'] = 'domain'
        response_users_get = requests.get('https://api.vk.com/method/users.get', params)
        result_users_get = response_users_get.json()['response'][0]['domain']
        link = 'https://vk.com/' + result_users_get
        return link

    def get_params(self):
        return {
            'access_token': token,
            'v': 5.92
        }

    def get_status(self,):
        params = self.get_params()
        params['user_id'] = self.source_uid
        response = requests.get('https://api.vk.com/method/status.get', params)
        return response.json()['response']['text']

    def set_status(self, text):
        params = self.get_params()
        params['text'] = text
        response = requests.get('https://api.vk.com/method/status.set', params)
        return response.json()['response'] == 1

    def __and__(self, id2):
        """
        :param id2: ID Вконтакте второго пользователя, с которым необходимо найти общий список друзей
        :return: Выводит список экземляров классов общих друзей
        """
        params = self.get_params()
        params['sourse_uid'] = self.source_uid
        params['target_uid'] = id2.__dict__['source_uid']
        response_get_mutual = requests.get('https://api.vk.com/method/friends.getMutual', params)
        result_get_mutual = list()
        for friend_id in response_get_mutual.json()['response']:
            result_get_mutual.append(User(friend_id))
        return result_get_mutual

print(User(11729201))
