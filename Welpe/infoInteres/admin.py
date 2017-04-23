# Register your models here.
from django.contrib import admin

from .models import InfoInteres


class InfoInteresAdmin(admin.ModelAdmin):
    def in_menu(self):
        return True

admin.site.register(InfoInteres, InfoInteresAdmin)
