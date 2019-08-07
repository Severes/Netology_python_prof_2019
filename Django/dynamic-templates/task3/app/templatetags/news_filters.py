from django import template
import datetime
import time


register = template.Library()


@register.filter
def format_date(value):
    value = time.ctime(value)
    value = datetime.datetime.strptime(value, "%a %b %d %H:%M:%S %Y")
    now = datetime.datetime.now()
    delta = (now - value).seconds
    result = ''
    if delta < 360:
        result = 'Меньше 10 минут'
    elif delta < 43200:
        result = f'{int(delta/3600)} часов назад'
    elif delta > 43200:
        result = datetime.datetime.strftime(value, "%Y-%m-%d")
    return result

@register.filter
def format_score(value):
    result = ''
    if value < -5:
        result = 'все плохо'
    elif -5 < value <= 5:
        result = 'нейтрально'
    elif value > 5:
        result = 'хорошо'
    return result


@register.filter
def format_num_comments(value):
    result = ''
    if value == 0:
        result = 'Оставьте комментарий'
    elif 0 < value <= 50:
        result = value
    elif value > 50:
        result = '50+'
    return result

@register.filter
def format_selftext(count, value):
    """
    Оставляет count первых и count последних слов, между ними должно быть троеточие.
    count задается параметром фильтра.
    Пример c count = 5: "Hi all sorry if this ... help or advice greatly appreciated."
    Знаки препинания остаются, обрезаются только слова.
    """
    pass






