
from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from models import (Portfolio,
                    PortfolioItem,
                    PortfolioItemImage,
                    PortfolioItemDetail,
                    PortfolioItemCategory)


class PortfolioItemImageInline(TabularDynamicInlineAdmin):
    model = PortfolioItemImage

class PortfolioItemDetailInline(TabularDynamicInlineAdmin):
    model = PortfolioItemDetail


class PortfolioItemAdmin(PageAdmin):
    inlines = (PortfolioItemImageInline, PortfolioItemDetailInline)


admin.site.register(Portfolio, PageAdmin)
admin.site.register(PortfolioItem, PortfolioItemAdmin)
admin.site.register(PortfolioItemCategory)
