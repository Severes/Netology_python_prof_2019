import datetime


class FileMerge:
    def __init__(self, path1, path2):
        self.path1 = path1
        self.path2 = path2
        self.start = datetime.datetime.now()

    def __enter__(self):
        with open(self.path1, encoding='utf-8') as file1:
            self.list1 = file1.readlines()
        with open(self.path2, encoding='utf-8') as file2:
            self.list2 = file2.readlines()
        self.list3 = self.list1 + self.list2
        self.list3.sort()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.datetime.now()
        print(exc_type)
        print(exc_val)
        print(exc_tb)
        print(self.end - self.start)

    def reverse(self):
        list_reversed = self.list3[:]
        list_reversed.reverse()
        return list_reversed

with FileMerge('list1.txt', 'list2.txt') as file_merge:
    print(file_merge.list3)
    print(file_merge.reverse())
    1/0
