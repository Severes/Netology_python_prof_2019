# Функция
def pw(x):
    return x * x

# Декоратор
def decorator(old_function):
    def new_function(x):
        sq = old_function(x)
        return sq * x
    return new_function


@decorator
def pw(x):
    return x * x


# print(pw(2))


# Как работают args и kwargs
def foo(*args, **kwargs):
    print(args)
    print('_______________')
    print(kwargs)


# foo(1, 2, 3, 4, a=100, b=200)

import datetime
import time

#Декоратор, который показывает времяработы функции.
def parametrized(multiplier):


    def bench(old_func):
        result = []
        def new_func(*args,**kwargs):
            start = datetime.datetime.now()
            ret = old_func(*args,**kwargs)
            end = datetime.datetime.now()
            res = end-start
            res = f'сек{res.seconds}'
            res = multiplier*res
            print(f'{old_func.__name__}: {res}')
            result.append(end-start)
            print(result)
            return ret
        return new_func
    return bench
#Функция
@parametrized(2)
def foo(x):
    time.sleep(x)



foo(2)
foo(2)
foo(2)

# Параметризованный дерокатор

# def multiply(multiplier):
#     summ = 0
#     count = 0
#     def decorator

# tdata = datetime.datetime.now()
# tdata.strftime('%Y')
# print(tdata)