from django.db import models
from mezzanine.core.fields import FileField
from mezzanine.core.fields import RichTextField
from django.utils.translation import ugettext as _
from mezzanine.core.models import RichText, Orderable
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to


class VideoHost:
    """
    Enum-like structure to determine the host of a video
    """
    Ninguno, Vimeo, Youtube = range(3)


class GenericContent(models.Model):
    def get_absolute_url(self):
        pass

    basicPage_id = models.AutoField(primary_key=True)
    showDate = models.BooleanField(_("Show date"), default=False)
    author = models.CharField(max_length=500, blank=True)
    summary = RichTextField(blank=True)
    image = models.ImageField(upload_to="contentImg", blank=True)
    image = FileField(verbose_name=_("Image"),
                               upload_to=upload_to("contentImg", "genericContent"),
                               format="Image", max_length=255, null=True, blank=True)
    image_footer = RichTextField(blank=True)
    video_footer = RichTextField(blank=True)
    hostVideo = models.SmallIntegerField(
        choices=(
            (VideoHost.Ninguno,
             "----"),
            (VideoHost.Youtube,
             "Youtube"),
            (VideoHost.Vimeo,
             "Vimeo"),),
        default=VideoHost.Ninguno, blank=True)
    video_id = models.CharField(
        max_length=255, null=True, help_text=_("The id of the video"), blank=True)


