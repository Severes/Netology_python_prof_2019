import json
import chardet
import os
from hashlib import md5

# Итератор
class CountryIter:
    def __init__(self, path):
        self.path = path
        self.file = open(path, encoding='utf-8')
        self.countries_list = json.load(self.file)
        self.start = 0
        self.end = len(self.countries_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self.start == self.end:
            raise StopIteration
        element = self.countries_list[self.start]
        country = element['name']['common']
        elementsplit = country.split()
        country_name = '_'.join(elementsplit)
        with open(os.path.splitext(self.path)[0] + '_and_links.txt', encoding='utf-8', mode='a') as new_text:
            c_string = '{} - {}'.format(country, 'https://en.wikipedia.org/wiki/' + country_name)
            print(c_string, file=new_text)
        self.start += 1
        return c_string

# Генератор:
def country_hash_gen(path):
    with open(path, encoding='utf-8') as text:
        while True:
            c_string = text.readline()
            if not c_string:
                break
            # yield c_string
            yield md5(c_string.encode('utf-8')).hexdigest()


if __name__ == '__main__':
# Запуск итератора
    for item in CountryIter('countries.json'):
        print(item)
# Запуск генератора
    for item in country_hash_gen('countries_and_links.txt'):
        print(item)