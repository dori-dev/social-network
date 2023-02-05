from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter(name='timesince')
def custom_timesince(value, arg=None):
    if not value:
        return ""
    try:
        if arg:
            value = timesince(value, arg)
        value = timesince(value)
    except (ValueError, TypeError):
        return ""
    return value.split('،', 1)[0]
