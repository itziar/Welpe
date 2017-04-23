from django.contrib import admin
from .models import Sitemap
# Register your models here.


class SitemapAdmin(admin.ModelAdmin):
	pass
#	fieldsets = (
#		(None, {
#			'fields': ('title','in_menus','in_sitemap')
#		}),
#
#	)

admin.site.register(Sitemap, SitemapAdmin)