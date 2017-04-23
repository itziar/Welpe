from django.contrib import admin

# Register your models here.
from mezzanine.core.admin import TabularDynamicInlineAdmin

from Welpe.basicModels.admin import GenericContentAdmin
from .models import BasicContent, ExternalLink, AttachedFile


class ExternalLinkInline(TabularDynamicInlineAdmin):
    model = ExternalLink


class AttachedFileInline(TabularDynamicInlineAdmin):
    model = AttachedFile


class BasicContentAdmin(GenericContentAdmin):
    fieldsets = (
        (None, {
            'fields': (
            'title', '_meta_title', 'slug', 'short_url', 'status', 'login_required', 'parent', '_order', 'publish_date',
            'expiry_date', 'showDate', 'author', 'in_menus', 'in_sitemap', 'keywords', 'gen_description', 'description',
            'summary', 'content', 'hostVideo', 'video_id', 'video_footer', 'image', 'image_footer')
        }),
    )
    inlines = (ExternalLinkInline, AttachedFileInline,)

    def in_menu(self):
        return True


admin.site.register(BasicContent, BasicContentAdmin)
