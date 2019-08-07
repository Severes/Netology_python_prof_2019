from django import template
import datetime
import time
import re


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
def format_selftext(value, count):
    split_list = re.findall('(\S+)', value)
    if len(split_list) > count*2:
        left_part = ' '.join(split_list[:count])
        right_part = ' '.join(split_list[-count:])
        center_str = '...'
        result = f'{left_part} {center_str} {right_part}'
    else:
        result = value
    return result






