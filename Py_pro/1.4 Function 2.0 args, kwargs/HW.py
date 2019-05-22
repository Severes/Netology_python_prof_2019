class Contact:
    def __init__(self, name, surename, phone, favorite=False, *args, **kwargs):
        self.name = name
        self.surename = surename
        self.phone = phone
        self.favorite = favorite
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        if self.favorite is True:
            self.favorite = 'Да'
        else:
            self.favorite = 'Нет'
        def kwarg(x):
            kwarg_list = list()
            for x_name, x_text in x.items():
                kwarg_list.append(f'        {x_name}: {x_text}')
            return '\n'.join(kwarg_list)
        info = f'Имя: {self.name}\nФамилия: {self.surename}\nТелефон: {self.phone}\nВ избранных: {self.favorite}\n' \
            f'Дополнительная информация:\n{kwarg(self.kwargs)}'
        return info


class PhoneBook:
    contact_list = list()
    def __init__(self, phonebook):
        self.phonebook = phonebook

    def new_contact(self, name, surename, phone, favorite=False, *args, **kwargs):
        new_contact_class = Contact(name, surename, phone, favorite, *args, **kwargs)
        self.contact_list.append(new_contact_class)
        return 'Контакт добавлен'

    def print_contact(self, contact_list_index):
        result = print(PhoneBook.contact_list[int(contact_list_index)])
        return result

    def delete_contact_by_phone_number(self, phonenumber):
        for contact in self.contact_list:
            if contact.phone == phonenumber:
                self.contact_list.remove(contact)
        result = print(f'Контакт с телефонным номером "{phonenumber}" удален из телефонной книги')
        return result

    def all_favorite_contacts(self):
        favorite_contact_list = list()
        for contact in self.contact_list:
            if contact.favorite is True:
                favorite_contact_list.append(contact.phone)
        str_list = '\n'.join(favorite_contact_list)
        result = print(f'Список избранных номеров:\n{str_list}')
        return result

    def contact_by_name_surename(self, cname, csurename):
        i = 1
        print(f'Список контактов с именем {cname} и фамилией {csurename}:')
        for contact in self.contact_list:
            if contact.name == cname and contact.surename == csurename:
                print(f'{i}\n{contact}')
                i += 1

# Создание телефонной книги
phonebook = PhoneBook('Справочник')

# Создание контактов
phonebook.new_contact('Vladimir', 'Simigin', '+79141785435', telegram='@simigin', email='v_mail@gmail.com')
phonebook.new_contact('Anastasia', 'Plazova', '+79238765789', favorite=True, telegram='@plazova', email='pl_mail@gmail.com')
phonebook.new_contact('Nikolai', 'Novikov', '+79140987878', favorite=True, telegram='@novikov', email='n_mail@gmail.com')
phonebook.new_contact('Artemiy', 'Lebedev', '+79152334555', favorite=True, telegram='@lebedev', email='l_mail@gmail.com')
phonebook.new_contact('Vladimir', 'Polskiy', '+79169008776', telegram='@polskiy', email='po_mail@gmail.com')
phonebook.new_contact('Artemiy', 'Lebedev', '+79152339875', favorite=True, telegram='@lebedev123', email='lebed_mail@gmail.com')

# Вывод всех избранных номеров
phonebook.all_favorite_contacts()

# Вывод информации по контакту
phonebook.print_contact(0)

# Удаление контакта по номеру телефона
phonebook.delete_contact_by_phone_number('+79141785435')

# Вывод информации по контакту
phonebook.print_contact(0)

# Вывод списка кнтактов по имени, фамилии
phonebook.contact_by_name_surename('Artemiy', 'Lebedev')
