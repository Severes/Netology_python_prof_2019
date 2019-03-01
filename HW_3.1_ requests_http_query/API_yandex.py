import os
import requests

URL = 'https://translate.yandex.net/api/v1/tr.json/translate'

params = {
    'id': '0978ab23.5c7987d6.d6d55a19-7-0',
    'srv': 'tr-text',
    'lang': 'ru-en',
    'reason': 'auto'
}

payload = {
    'text': 'Python удобен для быстрой разработки'
}

res = requests.post(URL, params=params, data=payload)

print(res.status_code)
print(res.json())