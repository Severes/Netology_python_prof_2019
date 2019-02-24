budget = 3000000
flat_price = '2700000'

# # Первый блок
# if type(flat_price) == int:
#     if flat_price < budget:
#         print('Не можем купить')
# else:
#     print('Это не число')

# # Второй блок
# try:
#     if flat_price < budget:
#         print('Не можем купить')
# except (TypeError, ZeroDivisionError) as e:
#     print(e)
# except Exception as e:
#     print(e)
# else:
#     print('Покупайте скорее!')
# finally:
#     print('Этот блок запуститься в любом случае')

# Третий блок
# if type(flat_price) != int:
#     flat_price = int(flat_price)
#     if flat_price < budget:
#         print('Не можем купить')

# # Четвертый блок
# try:
#     raise Exception('Наше тестовое исключение')
# except Exception as e:
#     print(e)
# print('Наш код работает дальше')

# # Пятый блок
# errors = [0, 1, 2]
#
#
# def division(a, b):
#     if b == 0:
#         raise ZeroDivisionError('Деление на ноль!')
#         # return (1, None)
#     return (0, a/b)
#
#
# print(division(1, 0))

# Шестой блок
# assert ужен для проверок. Например, переменных, как в примере ниже. Но, как мне кажется, лучше
# пользоваться оыбчным try except, или описанием отедльных типов иключений в except
fruits = ['orange', 'raspberry']
assert 'apple' in fruits
