# templatetags/future.py
from django import template


register = template.Library()


@register.filter
def getnames(value):
    if not value:
        return ""
    return value.name.split('/')[-1]


@register.assignment_tag
def has_permissions_info(info, user):
    try:
        grupo = user.groups.get()
    except:
        grupo = None
    if user.is_superuser or (grupo.name == "profesores") or (user == info.owner):
        return True
    else:
        return False
