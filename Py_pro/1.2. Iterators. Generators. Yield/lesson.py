import googletrans

x = [1, 2, 3]

# for item in x:
#     print(item)


# То, что на самом деле происходит в цикле for
# iterable = x.__iter__()
# print(iterable)
# print(iterable.__next__())
# print(iterable.__next__())
# print(iterable.__next__())

# Делаем итератор
# class RusEng:
#     def __init__(self, path):
#         self.file = open(path, encoding='utf-8')
#         self.translator = googletrans.Translator()
#
#     def __iter__(self):
#         return self
#
#     def __next(self):
#         word = self.file.readline()
#         if not word:
#                 raise StopIteration
#         word = self.
#
#
# # Синткксис генераторов
# def myrange(start, end):
#     while start < end:
#         yield start
#         start += 1


# Переводчик
def rus_eng(path):
    translator = googletrans.Translator()
    word = True
    with open(path, encoding='utf-8') as file:
        while True:
            word = file.readline()
            if not word:
                break
            yield translator.translate(word, dest='en', src='ru').text

gen = rus_eng('text.txt')
gen_iter = gen.__iter__()
print(gen_iter)
print(gen_iter.__next__())

print(rus_eng('text.txt'))

