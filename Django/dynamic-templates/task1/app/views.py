from django.shortcuts import render
import csv

def inflation_view(request):
    template_name = 'inflation.html'
    context = dict()
    with open('inflation_russia.csv', encoding='utf-8') as text:
        new_text = list(csv.reader(text, delimiter=';'))
        context['header'] = new_text[0]
        context['table'] = new_text[1:]
        return render(request, template_name,
                  context)