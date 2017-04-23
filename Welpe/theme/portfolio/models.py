
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to


COLUMNS_CHOICES = (
    ('6', 'Two columns'),
    ('4', 'Three columns'),
    ('3', 'Four Columns'),
)


class Portfolio(Page):
    '''
    A collection of individual portfolio items
    '''
    columns = models.CharField(max_length=1, choices=COLUMNS_CHOICES,
        default='3')
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")


PORTFOLIO_ITEM_LAYOUT_CHOICES = (
    (1, 'Slideshow/video above, content below'),
    (2, 'Slideshow/video on left, content on right'),
    (3, 'Slideshow/video on right, content on left'),
)


class PortfolioItem(Page, RichText):
    '''
    An individual portfolio item, should be nested under a Portfolio
    '''
    layout = models.PositiveIntegerField(choices=PORTFOLIO_ITEM_LAYOUT_CHOICES,
        default=1)
    description_heading = models.CharField(max_length=200,
                                           default="Project description")
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("theme.PortfolioItem.featured_image", "portfolio"),
        format="Image", max_length=255, null=True, blank=True)
    featured_video = models.TextField(blank=True,
        help_text= "Optional, putting video embed code (iframe) here, will "
                   "override a Featured image specified above.  This has "
                   "been tested to work with Youtube and Vimeo, but may "
                   "work with other iframes as well.")
    details_heading = models.CharField(max_length=200, default="Project details")
    categories = models.ManyToManyField("PortfolioItemCategory",
                                        verbose_name=_("Categories"),
                                        blank=True,
                                        related_name="portfolioitems")
    website = models.CharField(max_length=2000, blank=True,
        help_text="A link to the finished project or clients website "
                  " (optional)")
    related_items = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio items")


class PortfolioItemDetail(Orderable):
    '''
    Name/value mapping displayed in a tabular form.  I.E. Client: Awesome LLC, etc...
    '''
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="details")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)


class PortfolioItemImage(Orderable):
    '''
    An image for a PortfolioItem
    '''
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("theme.PortfolioItemImage.file", "portfolio"))
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def save(self, *args, **kwargs):
        if not self.portfolioitem.featured_image:
            self.portfolioitem.featured_image = self.file
            self.portfolioitem.save()
            if self.id:
               self.delete()
        else:
            super(PortfolioItemImage, self).save(*args, **kwargs)


class PortfolioItemCategory(Slugged):
    """
    A category for grouping portfolio items into a series.
    """

    class Meta:
        verbose_name = _("Portfolio Item Category")
        verbose_name_plural = _("Portfolio Item Categories")
        ordering = ("title",)

    def in_menu(self):
        return False