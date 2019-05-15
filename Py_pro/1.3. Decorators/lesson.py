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

def bench(old_func):
    count = 1
    def new_func(*args, **kwargs):
        nonlocal count
        start = datetime.datetime.now()
        ret = old_func(*args, **kwargs)
        end = datetime.datetime.now()
        print(f'{old_func.__name__}: {end-start} {count}')
        count += 1
        return ret
    return new_func

@bench
def foo(x):
    time.sleep(x)

# foo(3)
# foo(4)
# foo(5)


#Декоратор, который показывает времяработы функции.


def formatdata(timedelta):
    return f'{timedelta.seconds, timedelta.microseconds}'


def parametrized(func):

    def bench(old_func):
        result = []
        def new_func(*args,**kwargs):
            start = datetime.datetime.now()
            ret = old_func(*args,**kwargs)
            end = datetime.datetime.now()
            res = end-start
            # res = f'сек{res.seconds}'
            res = func(res)
            print(f'{old_func.__name__}: {res}')
            result.append(end-start)
            # print(result)
            return ret
        return new_func
    return bench

#Функция
@parametrized(formatdata)
def foo(x):
    time.sleep(x)

# foo(2)
# foo(2)
# foo(2)

import contextlib
import functools
class User:
    def __init__(self, uid):
        self.uid = uid



    @staticmethod
    def static():
        print(self)

    @classmethod
    def cmethod(cls, *uids):
        return [User(uid) for uid in uids]

    @property
    def _uid(self):
        return self.uid

user = User(10)

# print(user._uid)


def foo():
    """
    I am docstring
    """

def decor(old_func):
    @functools
    def new_func():
        x = old_func()
        return x
    return new_func
