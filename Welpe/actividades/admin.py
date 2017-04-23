# Register your models here.
from django.contrib import admin

from .models import Actividades, MiniActividad, OrganizadorMiniActividad, UsuariosRegistradosActividades
from mezzanine.core.admin import TabularDynamicInlineAdmin
from Welpe.basicModels.admin import GenericContentAdmin


class MiniActiviadInline(TabularDynamicInlineAdmin):
    model = MiniActividad

class OrganizadorMiniActividadInline(TabularDynamicInlineAdmin):
    model = OrganizadorMiniActividad


class ActividadesAdmin(GenericContentAdmin):
    inlines = (MiniActiviadInline,)

    def in_menu(self):
        return True

class MiniActividadAdmin(GenericContentAdmin):
    inlines = (OrganizadorMiniActividadInline,)

    def in_menu(self):
        return True


class UsuariosRegistradosActividadesAdmin(admin.ModelAdmin):
    def in_menu(self):
        return True


admin.site.register(Actividades, ActividadesAdmin)
admin.site.register(MiniActividad, MiniActividadAdmin)
admin.site.register(UsuariosRegistradosActividades, UsuariosRegistradosActividadesAdmin)
