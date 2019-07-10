import re
from pprint import pprint
import csv

with open("phonebook_raw.csv", encoding='utf8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# Переменные
patterns = [
    ['^(\w+)( |,)(\w+)( |,)(\w+|),(,+|)(,,,|[А-Яа-я]+)', r'\1,\3,\5,\7'],
    ['(\+7|8)\s*(\(|)(\d{3})[\s\)-]*(\d{3})\-*(\d{2})\-*(\d{2})', r'+7(\3)\4-\5-\6'],
    ['\(?доб\.\s(\d{4})\)*', r'доб.\1']
    ]

correct_list = []
del_str = []
contacts_list_str = []

for elem in contacts_list:
    elem2 = ','.join(elem)
    contacts_list_str.append(elem2)

for contact in contacts_list_str:
    for pattern in patterns:
        contact = re.sub(pattern[0], pattern[1], contact)
    correct_list.append(contact.split(','))

for i in range(1, len(correct_list) - 1):
    for m in range(i + 1, len(correct_list)):
        if correct_list[i][0] == correct_list[m][0]:
            for k in range(7):
                if correct_list[i][k] == '':
                    correct_list[i][k] = correct_list[m][k]
            del_str.append(correct_list[m])

for d in del_str:
    correct_list.remove(d)

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding='utf8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(correct_list)