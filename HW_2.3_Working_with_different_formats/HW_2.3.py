import json
import chardet
import xml.etree.ElementTree as xml


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


def xml_ten(file):
    tree = xml.parse(file)
    root = tree.getroot()
    description = root.findall('channel/item/description')
    all_news_text = str()
    six_digit_word_list = list()
    six_digit_word_list_count = list()
    hateful_10 = list()
    for desc in description:
        news_text = desc.text
        all_news_text += news_text
    all_news_text_list = all_news_text.split(' ')
    for word in all_news_text_list:
        if len(word) > 6:
            six_digit_word_list.append(word)
    for item in six_digit_word_list:
        x = item, six_digit_word_list.count(item)
        if x not in six_digit_word_list_count:
            six_digit_word_list_count.append(x)

    def sorted_key(key):
        return key[1]
    sorted_six_digit_count = sorted(six_digit_word_list_count, key=sorted_key, reverse=True)
    for a in range(10):
        item_list = list(sorted_six_digit_count[a])
        hateful_10.append(item_list[0])
    return hateful_10


print('10 максимально повторяющихся слов из файла JSON: ', json_ten('newsafr.json'))

print('10 максимально повторяющихся слов из файла XML:  ', xml_ten('newsafr.xml'))
