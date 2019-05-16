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

vladimir = Contact('Vladimir', 'Simigin', '+79141861116', telegram='@simigin', email='v.simigin@gmail.com')
print(vladimir)


class PhoneBook:
    contact_list = list()
    def __init__(self, phonebook):
        self.phonebook = phonebook

    def new_contact(self, ):


