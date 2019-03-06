from urllib.parse import urlencode


OAUTH_URL = 'https://oauth.vk.com/authorize'
APP_ID = 6887655


auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'status' 'friends' 'video',
    'response_type': 'token',
    'v': 5.92
}

# print(urlencode(auth_data))
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
token = 'e339aa5d615ad6f77ef9778b46bdb97a3973b9cd193bd00b543ae809fd8355a37840a5ac98cb126e2b7c3'

class User:

    def __init__(self, token):
        self.token = token

    def get_params(self):
        return {
            'token': self.token
            'v': 5.92
        }

    object.__and__(self, other)
        return self.