import datetime
from contextlib import contextmanager


@contextmanager
def merge_open(path1, path2):
    try:
        start= datetime.datetime.now()
        with open(path1, encoding='utf-8') as file1:
            list1 = file1.readlines()
        with open(path2, encoding='utf-8') as file2:
            list2 = file2.readlines()
        list3 = list1 + list2
        list3.sort()
        yield list3
    finally:
        end = datetime.datetime.now()
        print(end - start)


with merge_open('list1.txt', 'list2.txt') as merged:
    print(merged)
