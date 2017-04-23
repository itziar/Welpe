
from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.utils.admin import SingletonAdmin
from mezzanine.pages.admin import PageAdmin

from models import (SiteConfiguration,
                    HomePage, Slide, IconBox,
                    FAQ, FAQPage)

admin.site.register(SiteConfiguration, SingletonAdmin)


class SlideInline(TabularDynamicInlineAdmin):
    model = Slide


class IconInline(TabularDynamicInlineAdmin):
    model = IconBox


class HomePageAdmin(PageAdmin):
    inlines = (SlideInline, IconInline)


admin.site.register(HomePage, HomePageAdmin)

class FAQInline(TabularDynamicInlineAdmin):
    model = FAQ
    extra = 50


class FAQPageAdmin(PageAdmin):
    inlines = (FAQInline,)


admin.site.register(FAQPage, FAQPageAdmin)