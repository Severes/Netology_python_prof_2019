import datetime
import json
import chardet


def path_logger_func(path):
    def logger(old_func):
        def new_func(*args, **kwargs):
            start = datetime.datetime.now()
            name_func = old_func.__name__
            func_args = args
            func_kwargs = kwargs
            res = old_func(*args, **kwargs)
            with open(path, encoding='utf-8', mode='a') as text:
                print(f'Название функции - {name_func}', file=text)
                print(f'Время старта функции - {start}', file=text)
                print(f'Аргументы функции - {func_args}, {func_kwargs}', file=text)
                print(f'Результат - {res}', file=text)
                print('------------', file=text)
            succes = print(f'Данные выполнения функции записаны в файл: {path}')
            return succes
        return new_func
    return logger

@path_logger_func('log.txt')
def json_ten(file):
    # Открываем файл и считываем весь текст построчно, попутно вычисляя кодировку
    with open(file, 'rb') as text:
        text2 = text.read()
        result = chardet.detect(text2)
        # На этот раз открываем файл в уже правильной кодировке, полученной из предыдущего файла
        with open(file, encoding=result['encoding']) as text:
            six_digit_list = list()
            movie = json.load(text)  # изменят файл с JSON формата в формат Python
            i = 0
            movie_full_text = ''
            items_len = len(movie['rss']['channel']['items'])  # выходим на уровень списка items и просматриваем,
            # сколько в нем элементов.
            # Перебираем каждый элемент списка items, вытаскиваем значение ключа description и включаем в общий текст
            for i in range(items_len):
                movie_channel_description = movie['rss']['channel']['items'][i]['description']
                movie_full_text += movie_channel_description + ' '
                i += 1
            movie_full_text_list = movie_full_text.split(' ')  # Делаем список слов из единой строки текста. Это
            # необходимо, потому что строка неизменяемый объект и его не получится перебрать циклом
            for word in movie_full_text_list:
                if len(word) > 6:
                    six_digit_list.append(word)
        # Считаем повторения слов в списке и создаем список из значения и его количества в списке
        six_digit_list_count = list()
        for item in six_digit_list:
            x = item, six_digit_list.count(item)
            if x not in six_digit_list_count:
                six_digit_list_count.append(x)

        # Функция, которая поможет отсортировать значения в списке в зависимости от количества повторений слов в списке
        def sorted_key(key):
            return key[1]
        # Сортируем список по количеству повторений значений этого списка
        sorted_six_digit_list_count = sorted(six_digit_list_count, key=sorted_key, reverse=True)
        # Ниже мы элементы итогового списка превращаем в списки и выводим первый элемент этого списка
        hateful_10 = list()
        for a in range(10):
            item_list = list(sorted_six_digit_list_count[a])
            hateful_10.append(item_list[0])
        # Выводим итоговый список строк
        return hateful_10


json_ten('newsafr.json')