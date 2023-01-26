import re
from django import template
from django.utils.html import format_html
from custom.utils import get_menu_items
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import (PAGE_VAR)

register = template.Library()
assignment_tag = register.assignment_tag if hasattr(
    register, 'assignment_tag') else register.simple_tag


@register.filter
def clean_text(value):
    res = value.replace('\n', ' ')
    return res


@register.filter
def checkbox(value):
    res = re.sub(r"</?(?i:td)(.|\n)*?>", "", value)
    return res


@assignment_tag(takes_context=True)
def admin_get_menu(context):
    return get_menu_items(context)


@register.simple_tag
def paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == cl.paginator.ELLIPSIS:
        return format_html('{} ', cl.paginator.ELLIPSIS)
    elif i == cl.page_num:
        return format_html('<a href="" class="page-link">{}</a> ', i)
    else:
        return format_html(
            '<a href="{}" class="page-link {}">{}</a> ',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe('end' if i == cl.paginator.num_pages else ''),
            i,
        )


@register.filter
def sum_number(value, number):
    return value + number


@register.filter
def neg_num(value, number):
    return value - number
