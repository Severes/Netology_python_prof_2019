# В функции нет вывода, так как явызываю даннуюфункцию во второй задаче ДЗ
"""
Должны получить следующее:

cook_book = {
  'Омлет': [
    {'ingridient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
    {'ingridient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
    {'ingridient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
    ],
  'Утка по-пекински': [
    {'ingridient_name': 'Утка', 'quantity': 1, 'measure': 'шт'},
    {'ingridient_name': 'Вода', 'quantity': 2, 'measure': 'л'},
    {'ingridient_name': 'Мед', 'quantity': 3, 'measure': 'ст.л'},
    {'ingridient_name': 'Соевый соус', 'quantity': 60, 'measure': 'мл'}
    ],
  'Запеченный картофель': [
    {'ingridient_name': 'Картофель', 'quantity': 1, 'measure': 'кг'},
    {'ingridient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'},
    {'ingridient_name': 'Сыр гауда', 'quantity': 100, 'measure': 'г'},
    ]
  }
"""


def reading_recipe():
    with open('recipes.txt', encoding='utf-8') as text:
        cook_book = dict()
        ingredients_list = list()
        for row in text:
            if row != '\n':
                dish_row = row.strip()
                cook_book[dish_row] = list()
                ingredient_count_row = text.readline().strip()
                i = 0
                while True:
                    i += 1
                    ingredient_row = text.readline().strip()
                    ingredients_list.append(ingredient_row)
                    dish_keys = ['ingredient_name', 'quantity', 'measure']
                    dish_values = ingredient_row.split(' | ')
                    ingredient_items = dict(zip(dish_keys, dish_values))
                    cook_book[dish_row].append(ingredient_items)
                    if i < int(ingredient_count_row):
                        continue
                    else:
                        break
    return cook_book


reading_recipe()
