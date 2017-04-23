from django import template
from mezzanine.conf import settings
from datetime import date
register = template.Library()


@register.assignment_tag
def has_permissions_profile(profile, user):
    if user.is_superuser or (user == profile):
        return True
    else:
        return False


@register.assignment_tag
def has_permissions(user):
    try:
        grupo = user.groups.get()
    except:
        grupo = None
    if user.is_superuser or (grupo.name == "profesores"):
        return True
    else:
        return False
