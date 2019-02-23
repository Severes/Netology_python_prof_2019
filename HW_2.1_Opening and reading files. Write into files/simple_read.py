with open('hello.txt', encoding='utf-8') as text:

    # for i in range(5):
    #     print('Следующая строка')
    #     print(text.readline().strip())

    for line in text:
        print('Следующая строка:')
        print(line.strip())

print('Файл закрыт? {}'.format(text.closed))
