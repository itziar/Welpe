# templatetags/future.py
from django import template

register = template.Library()

@register.filter
def getnames(value):
    if not value:
        return ""
    return value.name.split('/')[-1]
