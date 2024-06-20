# ecommerce/templatetags/custom_tags.py
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, url_name):
    request = context['request']
    if request.path == url_name:
        return 'active'
    return ''
