from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def hello_view(request):
    return HttpResponse('Hello')

def hello_name_view(request):
    name = request.GET.get('name', 'Анонимус')
    print(request.GET)
    hello_msg = f'Привет, {name}'
    return HttpResponse(hello_msg)

def since_view(request, year, month, day):
    since_str = f'{year}-{month}-{day}'
    now = datetime.now().date()
    since_date = datetime(year=year, month=month, day=day).date()
    # print(now, since_date)
    delta = now - since_date
    if since_date> now:
        return HttpResponse('Дата еще не наступила')

    since_str = f'С даты {since_date} прошло {delta.days} дней'
    return HttpResponse(since_str)