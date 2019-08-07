from django import template
from decimal import Decimal
register = template.Library()

@register.filter
def val_int(value):
    return Decimal(value)