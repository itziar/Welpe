# templatetags/future.py
from django import template
from Welpe.manageUser.views import User
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.filter
def getnames(value):
    if not value:
        return ""
    return value.name.split('/')[-1]


@register.assignment_tag
def has_permissions_propuesta(propuesta, user):
    try:
        grupo = user.groups.get()
    except:
        grupo = None
    if user.is_superuser or (grupo.name == "profesores") or (user == propuesta.usuario):
        return True
    else:
        return False





@register.assignment_tag
def get_name(user):
    if not user:
        return ""
    if user:
        return user.username.split("@")[0]
    return user.username


@register.assignment_tag
def get_name_from_str(username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist, e:
        raise Exception (e)

    if user:
        return user.email.split("@")[0]
    retornar=user.first_name+" "+user.last_name
    return retornar

@register.assignment_tag
def get_mail(user):
    if not user:
        return ""
    return user

