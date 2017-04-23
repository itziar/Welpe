# Register your models here.
from django.contrib import admin

from .models import OfertaTrabajo
from mezzanine.core.admin import TabularDynamicInlineAdmin


class OfertasTrabajoAdmin(admin.ModelAdmin):
    def in_menu(self):
        return True

admin.site.register(OfertaTrabajo, OfertasTrabajoAdmin)
