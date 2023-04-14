import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def render(content):
    content = re.sub(r"#(\w+)", r"<a href='/posts/tag/\1/'>#\1</a>", content)
    return mark_safe(content)


@register.filter
def split_string(value: str):
    return value.split()
