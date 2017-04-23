
from mezzanine.pages.page_processors import processor_for

from .models import HomePage
from Welpe.theme.portfolio.models import PortfolioItem

@processor_for(HomePage)
def home_processor(request, page):
    # si quiero diferencia de la home entre usuarios autenticados y los que no
    '''if not request.user.is_authenticated():
        return render(request, template_name="pages/index-login.html")
    else:'''
    homepage = HomePage.objects.prefetch_related(
        'slides', 'boxes').select_related(
        'featured_portfolio', 'featured_gallery').get(id=page.homepage.id)
    items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=homepage.featured_portfolio)[:homepage.max_portfolio_items]
    return {"homepage": homepage, 'items': items}
