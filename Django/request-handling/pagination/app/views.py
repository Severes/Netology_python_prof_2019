import csv
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from . import settings
from urllib.parse import urlencode
from django.core.paginator import Paginator

path = settings.BUS_STATION_CSV


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    context = dict()
    with open(path, encoding='cp1251') as csv_text:
        new_text = list(csv.DictReader(csv_text))
    paginator = Paginator(new_text, 10)
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    page_stations = paginator.page(page)
    stations = page_stations.object_list
    context = {
        'bus_stations': stations,
        'current_page': page,
    }

    if page > 1:
        context['prev_page_url'] = 'bus_stations?' + urlencode({'page': page - 1})
    else:
        context['prev_page_url'] = None
    if page != paginator.count:
        context['next_page_url'] = 'bus_stations?' + urlencode(({'page': page + 1}))
    else:
        context['next_page_url'] = None
    return render_to_response('index.html', context)


