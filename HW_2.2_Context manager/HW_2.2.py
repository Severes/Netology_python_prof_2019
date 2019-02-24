import datetime
"""
Программа показывает какие символы относятся к кириллице. Остальные символы заменяются на "*"
Желательно в исходный файл "text.to.check.txt"
(https://github.com/Severes/Netology_python_prof_2019/blob/master/HW_2.2_Context%20manager/text_to_check.txt) 
помещать небольшое количество текста, чтобы он умещался в одну строку. 
Так будет наглядно видно, какие символы необходимо заменить.
"""


class CheckingKeyBoardLayout:
    def __init__(self, path):
        self.path = path
        self.start = datetime.datetime.now()

    def __enter__(self):
        cyrilic_dict = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        cyrilic = list()
        with open(self.path, encoding='utf-8') as text:
            self.checking_text = text.read()
            for l in self.checking_text:
                if l in cyrilic_dict.lower():
                    cyrilic.append(l.upper())
                else:
                    cyrilic.append('*')
            self.text_from_file = print('\nИсходный текст: ', self.checking_text.upper())
            self.checked_text = print('Кириллица:      ', ''.join(cyrilic))
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.datetime.now()
        print('\nВремя начала выполнения программы: ', self.start)
        print('Время окончания выполнения программы: ', self.end)
        print('Время выполнения программы: ', self.end - self.start)


with CheckingKeyBoardLayout('text_to_check.txt') as final_text:
    final_text.text_from_file
    final_text.checked_text
