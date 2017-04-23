# templatetags/future.py
from __future__ import unicode_literals



from django.core.exceptions import ObjectDoesNotExist
from mezzanine import template
from mezzanine.accounts.views import User
register = template.Library()

@register.filter
def getnames(value):
    if not value:
        return ""
    return value.name.split('/')[-1]


@register.assignment_tag
def has_permissions_actividad(actividad, user):
    try:
        grupo = user.groups.get()
    except:
        grupo = None
    if user.is_superuser or (grupo.name == "profesores")  or (user == actividad.owner) or (user.email in actividad.adminlist):
            return True
    return False


@register.assignment_tag
def get_name(user):
    if not user:
        return ""
    if not user.first_name or user.first_name == " ":
        return user.username.split("@")[0]
    return user.first_name+" "+user.last_name


@register.assignment_tag
def get_name_from_str(username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist, e:
        raise Exception (e)

    if not user.first_name or user.first_name == " ":
        return user.email.split("@")[0]
    retornar=user.first_name+" "+user.last_name
    return retornar

@register.assignment_tag
def get_mail(user):
    if not user:
        return ""
    return user.email


