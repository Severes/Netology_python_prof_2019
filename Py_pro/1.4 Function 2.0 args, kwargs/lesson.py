def foo(x):
    return x * x


# print(dir(foo))


# ТАК ДЕЛАТЬ НЕ НУЖНО!!!
# class Foo:
#     def __call__(selfself, x):
#         print(x)
#
# foo = Foo()
#
# foo('hi')

# print(callable(len))
# print(callable(14))

def fabric(multiplayer):
    def foo():
        return 2 * multiplayer
    return foo


funcs = [fabric(i) for i in range(10)]
# print(funcs)

# print(funcs[0]())

"""
У функции может быть 4 вида аргументов:
1. Обязательные
2. Необзятельные
3. Необязательные неименованныеаргументы - *args
4. Необязательные именованные аргументы - **kwargs
"""

def foo(a, b=1, *args, **kwargs):
    print(locals())
    print(a)
    print(b)
    print(args)
    print(kwargs)

foo('first', 2, 10, 20, 30, c=15, z=77)

"""
Lambda функции

1. lambda - это анонимная функция. Может содержать лишь одно вырадение
Пример:
a.(lambda x, y: x * y)(1,2)

2. Lambda часто используется в функции sorted
Пример:
а. print(sorted({5:'a', 3:'b', 0:'c'}.items(), key=lambda x: x[1]))

3. Давайте улучшим нашу фабрику умножения
"""

import random

# def foo(x):
#     return random.randrange(0, x)

first = list(map(lambda x: random.randrange(0, x), range(1, 100)))
second = list(map(lambda x: random.randrange(0, x), range(1, 100)))

fin = list(zip(first, second))
fin.sort(key=lambda x: x[1])
# print(fin)
#
# print(first)
# print(second)
# print(list(fin))

def fabric(multiplier):
    return lambda : 2 * multiplier

funcs = {i:fabric(i) for i in range(0, 10)}

print(funcs[1]())



"""
__annotations__
"""

def get_data(_id:'Это id пользователя', n:int, force:bool) -> int:
    """
    Эта функция делает что-то
    """
    return n*n

print(get_data.__annotations__)
print(help(get_data))

print(get_data)