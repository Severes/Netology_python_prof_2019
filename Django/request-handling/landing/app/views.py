from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    if request.GET.get('from-landing') == 'original':
        counter_click['original'] += 1
    elif request.GET.get('from-landing') == 'test':
        counter_click['test'] += 1
    context = {
        'click_original': counter_click['original'],
        'click_test': counter_click['test']
    }
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    return render_to_response('index.html', context)


def landing(request):
    if request.GET.get('ab-test-arg') == 'original':
        counter_show['original'] += 1
        return render_to_response('landing.html')
    elif request.GET.get('ab-test-arg') == 'test':
        counter_show['test'] += 1
        return render_to_response('landing_alternate.html')
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов


def stats(request):
    try:
        test = counter_click['test'] / counter_show['test']
    except ZeroDivisionError:
        test = 0

    try:
        original = counter_click['original']/counter_show['original']
    except ZeroDivisionError:
        original = 0

    context = {
        'test_conversion': test,
        'original_conversion': original
    }
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    return render_to_response('stats.html', context)
