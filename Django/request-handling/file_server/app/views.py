import datetime
import os
from django.shortcuts import render
from . import settings

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
        files.append(file_dict)
    context['files'] = files

    if date:
        context['date'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return render(request, template_name, context)


def file_content(request, name):
    context = dict()
    context['file_name'] = name
    with open(path + '/' + name, encoding='utf-8') as file_text:
        context['file_content'] = file_text.read()
    return render(
        request,
        'file_content.html',
        context
    )

