from django import template
from store.models import Product  

register = template.Library()

@register.filter
def smart_truncate(value, length=18):
    if len(value) > length:
        return value[:length] + '...'
    else:
        return value

@register.filter
def pesewas_to_cedis(value):
    try:
        return float(value) / 100
    except (ValueError, TypeError):
        return 0

@register.filter
def lowercase(value):
    try:
        return value.lower()
    except (ValueError, TypeError):
        return "lowercase only works on strings"

@register.filter
def increment(number):
    return number + 1
