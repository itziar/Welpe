
from django.conf import settings

from mezzanine import template
from mezzanine.utils.sites import current_site_id

from Welpe.theme.models import SiteConfiguration

# templatetags/future.py
from django.template.defaulttags import cycle as cycle_original



register = template.Library()

@register.filter
def can_view_help(user):
    # if settings.DEBUG or user.has_site_permission:
    #    return True
    return False


@register.as_tag
def get_site_conf():
    """
    Adds the `SiteConfiguration` to the context
    """
    return SiteConfiguration.objects.get_or_create(site_id=current_site_id())[0]


@register.tag
def cycle(*args, **kwargs):
    ''' A stub to get SortableTabularInline to work '''
    return cycle_original(*args, **kwargs)
