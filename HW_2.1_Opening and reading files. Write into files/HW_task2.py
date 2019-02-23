from HW_task1 import reading_recipe

# Нужно написать функцию, которая на вход принимает список блюд из cook_book и количество персон для кого мы будем готовить
#
# get_shop_list_by_dishes(dishes, person_count)
# На выходе мы должны получить словарь с названием ингредиентов и его количетсва для блюда. Например, для такого вызова
#
# get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
# Должен быть следующий результат:
#
# {
#   'Картофель': {'measure': 'кг', 'quantity': 2},
#   'Молоко': {'measure': 'мл', 'quantity': 200},
#   'Помидор': {'measure': 'шт', 'quantity': 8},
#   'Сыр гауда': {'measure': 'г', 'quantity': 200},
#   'Яйцо': {'measure': 'шт', 'quantity': 4},
#   'Чеснок': {'measure': 'зубч', 'quantity': 6}
# }
# Обратите внимание, что ингредиенты могут повторяться


def main_input():
    dishes_input = input('Введите блюда через пробел: ')
    dishes_list = dishes_input.split()
    dishes = list()
    for elem in dishes_list:
        dishes.append(elem.capitalize())
    person_count = input('Введите количество человек: ')
    return get_shop_list_by_dishes(dishes, person_count)


def get_shop_list_by_dishes(dishes, person_count):
    cook_book = reading_recipe()

    return print(cook_book)


main_input()

