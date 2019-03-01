import os
import requests
from pprint import pprint
"""
API Apple
Скачиваем картинки для альбомов и сохраняем их в папку covers
"""

URL = 'https://itunes.apple.com/search'
params = {
    'term': 'coldplay'
}

res = requests.get(URL, params)


print('status_code', res.status_code)
print('raise_for_status', res.raise_for_status())
# print('content', res.content)  # content получает данные в формате для бинарника (типо картинки)
print('json', res.json().keys())
data = res.json()['results']
print('data', data)
for item in data:
    # print(f'{item["trackName"]} - {item["artistName"]} - {item["artworkUrl100"]}')
    print('{} - {} - {}'.format(item['trackName'], item['artistName'], item['artworkUrl100']))
    filename = '{} - {}'.format(item['trackName'], item['artistName']) + '.jpg'
    filename_path = os.path.join('covers', filename)
    with open(filename_path, 'wb') as text:
        img_res = requests.get(item['artworkUrl100'])
        text.write(img_res.content)
        print('Сохранено в {}'.format(filename_path))

