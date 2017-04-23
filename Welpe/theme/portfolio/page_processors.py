
from mezzanine.pages.page_processors import processor_for
from .models import Portfolio, PortfolioItem, PortfolioItemCategory

@processor_for(Portfolio)
def portfolio_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page)
    categories = PortfolioItemCategory.objects.filter(portfolioitems__in=items).distinct()
    return {'items': items, 'categories': categories}


@processor_for(PortfolioItem)
def portfolioitem_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    prortfolioitem = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related(
        'categories', 'related_items', 'images', 'details').get(id=page.portfolioitem.id)
    return {'portfolioitem': prortfolioitem}
