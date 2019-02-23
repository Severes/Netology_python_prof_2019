from HW_task1 import reading_recipe
from pprint import pprint
"""
Нужно написать функцию, которая на вход принимает список блюд из cook_book и количество персон для кого мы будем готовить

get_shop_list_by_dishes(dishes, person_count)
На выходе мы должны получить словарь с названием ингредиентов и его количетсва для блюда. Например, для такого вызова

get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
Должен быть следующий результат:

{
  'Картофель': {'measure': 'кг', 'quantity': 2},
  'Молоко': {'measure': 'мл', 'quantity': 200},
  'Помидор': {'measure': 'шт', 'quantity': 4},
  'Сыр гауда': {'measure': 'г', 'quantity': 200},
  'Чеснок': {'measure': 'зубч', 'quantity': 6}
  'Яйцо': {'measure': 'шт', 'quantity': 4},
}
Обратите внимание, что ингредиенты могут повторяться
"""


def main_input():
    try:
        dishes_input = input('Введите блюда через запятую-пробел (", "): ')
        dishes_list = dishes_input.split(', ')
        dishes = list()
        for elem in dishes_list:
            dishes.append(elem.capitalize())
            person_count = int(input('Введите количество человек: '))
    except:
        print('Что-то пошло не так, повторите ввод')
        main_input()
    return get_shop_list_by_dishes(dishes, person_count)


def get_shop_list_by_dishes(dishes, person_count):
    cook_book = reading_recipe()
    shop_list = dict()
    for dish in dishes:
        if dish in cook_book.keys():
            for ingredient in cook_book[dish]:
                new_ingredient = dict(ingredient)
                new_ingredient['quantity'] = int(ingredient['quantity'])
                new_ingredient['quantity'] *= person_count
                if new_ingredient['ingredient_name'] not in shop_list:
                    shop_list[new_ingredient['ingredient_name']] = new_ingredient
                else:
                    shop_list[new_ingredient['ingredient_name']]['quantity'] += new_ingredient['quantity']
                del new_ingredient['ingredient_name']
    result = pprint(shop_list)
    return result


main_input()

