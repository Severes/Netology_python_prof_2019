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
    result = print(cook_book)
    return result


def main_input():
    dishes_input = input('Введите блюда через пробел: ')
    dishes_list = dishes_input.split()
    dishes = list()
    for elem in dishes_list:
        dishes.append(elem.capitalize())
    person_count = input('Введите количество человек: ')
    return()

# def get_shop_list_by_dishes(dishes, person_count):

main_input()