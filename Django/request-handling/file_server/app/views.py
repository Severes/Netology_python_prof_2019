import datetime
import os
from django.shortcuts import render
from . import settings
from django.http import HttpResponse

path = settings.FILES_PATH
project_files = os.listdir(path)

def file_list(request, date=None):
    context = dict()
    template_name = 'index.html'
    files = list()
    for file in project_files:
        file_dict = dict()
        file_dict['name'] = file
        file_dict['ctime'] = datetime.datetime.fromtimestamp(os.stat(f'{path}/{file}').st_ctime)
        file_dict['mtime'] = datetime.datetime.fromtimestamp(os.stat(f'{path}/{file}').st_mtime)
        if date == None:
            files.append(file_dict)
        else:
            context['date'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            if file_dict['ctime'].date() == context['date']:
                files.append(file_dict)
    context['files'] = files
    return render(request, template_name, context)


def file_content(request, name):
    context = dict()
    file_path = os.path.join(path, name)
    context['file_name'] = name
    if os.path.exists(file_path):
        with open(file_path, encoding='utf-8') as file_text:
            context['file_content'] = file_text.read()
        return render(
        request,
        'file_content.html',
        context
    )
    else:
        return HttpResponse('Файл не существует')

