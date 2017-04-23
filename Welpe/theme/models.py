
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import Orderable, SiteRelated
from mezzanine.galleries.models import Gallery
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to

from portfolio.models import Portfolio


RIGHT = 'RI'
LEFT = 'LE'
SIDEBAR_ALIGNMENTS = (
    (LEFT, _('Left')),
    (RIGHT, _('Right')),
)

BLOG_LAYOUTS = (
    (1, _('One')),
    (2, _('Two')),
)


CONTACT_IFRAME_CHOICES = (
    ('FULL', _('Full width')),
    ('PAGE', _('Page width')),
)


class SiteConfiguration(SiteRelated):
    '''
    Editable, sitewide content/settings
    '''
    color_scheme = models.PositiveIntegerField(default=3,
        help_text="Use the cog icon in the front end to try out color "
                  "schemes.")
    sidebar_alignment = models.CharField(max_length=2,
        choices=SIDEBAR_ALIGNMENTS, default='RI',
        help_text="For pages that have a sidebar, determines if it is on the "
                  "left or right")
    default_sidebar = models.TextField()
    blog_layout = models.PositiveIntegerField(choices=BLOG_LAYOUTS, default=2,
        help_text="Determines how many blog posts are shown per row in the "
                  "blog list view")
    footer_description = RichTextField()
    footer_blog_heading = models.CharField(max_length=100, default="Recent posts")
    footer_menu_heading = models.CharField(max_length=100, default="Popular pages")
    footer_flickr_heading = models.CharField(max_length=100, default="Flickr photos")
    footer_flickr_content =  RichTextField(blank=True,
        help_text="If present will override the flickr widget in the footer")
    contact_iframe = models.TextField(blank=True,
        help_text="If present any form with slug contact will displayed with "
                  "a custom template that has this iframe at the top. i.e. "
                  "add a Google Map's iframe here.")
    contact_iframe_layout = models.CharField(max_length=4, blank=True,
        default="FULL", choices=CONTACT_IFRAME_CHOICES)

    class Meta:
        verbose_name = _('Site Configuration')
        verbose_name_plural = _('Site Configuration')


ICON_BOX_LAYOUT_CHOICES = (
    ('TW', 'Two across'),
    ('TH', 'Three across'),
    ('TB', 'Three across boxes'),
)


class HomePage(Page):
    '''
    A page representing the format of the home page
    '''
    #featured_portfolio = models.ForeignKey("Portfolio", blank=True, null=True,
    #    help_text="If selected items from this portfolio will be featured "
    #              "on the home page.")
    featured_portfolio_heading = models.CharField(max_length=100, blank=True,
        default="Recent works",
        help_text="If present and featured_portfolio is set portfolio "
                  "items will be shown with this header.")
    featured_portfolio = models.ForeignKey(Portfolio, blank=True, null=True)
    max_portfolio_items = models.PositiveIntegerField(blank=True, null=True,
        default=6,
        help_text="The maximum number of items from the above selected portoflio to show.")
    icon_box_layout = models.CharField(max_length=2,
        choices=ICON_BOX_LAYOUT_CHOICES, default="TH")
    recent_blog_heading = models.CharField(max_length=100, blank=True,
        default="Latest blog posts",
        help_text="If present recent blog posts will be shown")
    breakout_heading = models.CharField(max_length=200, blank=True)
    breakout_content = RichTextField(blank=True)
    breakout_button_text = models.CharField(max_length=200, blank=True)
    breaktou_button_link = models.CharField(max_length=2000, blank=True)
    featured_gallery_heading = models.CharField(max_length=100, blank=True,
        default="Our clients",
        help_text="If present and featured_gallery is selected a carousel of "
                  "the gallery images will be shown with this title.")
    featured_gallery = models.ForeignKey(Gallery, blank=True, null=True)

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Slide(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="slides")
    background = FileField(verbose_name=_("Background Image"),
        upload_to=upload_to("theme.Slide.image", "slider"),
        format="Image", max_length=255, blank=True)
    heading = models.CharField(max_length=100, blank=True)
    subheading = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True,
        help_text="Add <br> for line breaks")
    button_text = models.CharField(max_length=100, blank=True,
        help_text="Optional, if present a button with the link specified "
                  "below will be in the slide")
    button_link = models.CharField(max_length=2000, blank=True)
    image = FileField(verbose_name=_("Image"),
        upload_to=upload_to("theme.Slide.image", "slider"),
        format="Image", max_length=255, blank=True)
    custom = models.TextField(blank=True,
        help_text="Create a custom slide, everything else will be overriden")


class IconBox(Orderable):
    '''
    An icon box on a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="boxes")
    icon = models.CharField(max_length=50,
        help_text="Enter the name of a font awesome icon, i.e. "
                  "fa-eye. A list is available here "
                  "http://fontawesome.io/")
    title = models.CharField(max_length=100)
    content = RichTextField()
    link = models.CharField(max_length=2000, blank=True,
        help_text="Optional, if provided clicking the box will go here.")


class FAQPage(Page):
    '''
    A page of FAQs
    '''
    content = RichTextField(blank=True)

    class Meta:
        verbose_name = _("FAQ page")
        verbose_name_plural = _("FAQ pages")


class FAQ(Orderable):
    '''
    A FAQ on a FAQ Page
    '''
    faqpage = models.ForeignKey(FAQPage, related_name="faqs")
    question = models.CharField(max_length=300)
    answer = RichTextField()
