import requests
import os


def translate(file, text, lang_from, lang_to):
    """
    :param file: имя открываемого файла
    :param text: текст файла file
    :param lang_from: язык, с которого переводим
    :param lang_to: язык, на который переводим
    :return: создает новый документ, в который вставляет переведенный текст
    """
    text_parts = list()
    translated_text = list()
    x = 0
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152',
        'srv': 'tr-text',
        'lang': '{}-{}'.format(lang_from, lang_to),
        'reason': 'auto'
    }
    # пока длина списка text_parts в символах не станет станет равна длине текста из файла file
    # данный цикл будет резать длину текста файла и помещать эти части в виде элементов списка text_parts
    while len(''.join(text_parts)) < len(text):
        y = x + 500
        text_parts.append(text[x:y])
        x += 500
    # данный цикл берет каждую часть списка text_parts и отправляет запросом post данный текст через API Яндекс
    # переводчик. Затем часть уже переведенного текста вставляется в список translated_text
    for part in text_parts:
        data = {
            'text': str(part)
        }
        response = requests.get(
            URL, params=params, data=data)
        translated_text.append(''.join(response.json()['text']))
    with open(os.path.splitext(file)[0]+'_TRANSLATED.txt', encoding='utf-8', mode='w') as text_new:
        # записываем выводимый текст в созданный файл
        print(''.join(translated_text), file=text_new)
        print('Текст был переведен и записан в файл: ', os.path.splitext(file)[0]+'_TRANSLATED.txt')


def set_params():
    """
    Запрашивает данные у пользователя
    Открывает документ и считывает текст
    :return: запускает функцию translate() по работе с API Яндекс Переводчик
    """
    file = input('Введите название файла, который необходимо перевести: ')
    lang_from = input('Введите язык, с которого нужно перевести: ')
    lang_to = input('Введите язык, на который нужно перевести (по-умолчанию русский): ')
    # проверяем язык, на который нужно переводить
    if lang_to == '':
        lang_to = 'ru'
    # вытаскиваем текст из файла
    with open(file, encoding='utf-8') as text_file:
        text = text_file.read()
    return translate(file, text, lang_from, lang_to)


set_params()
