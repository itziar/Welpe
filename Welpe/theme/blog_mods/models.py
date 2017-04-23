
from django.db import models
from django.utils.translation import ugettext_lazy as _

from blog.models import BlogPost
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable
from mezzanine.utils.models import upload_to


class BlogPostImage(Orderable):
    '''
    An image for a BlogPost slideshow
    '''
    blog_post = models.ForeignKey(BlogPost, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("mezzanine.blog.BlogPost.file", "blog"))
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _("Slideshow (will only display if a featured video "
                         "is not specified above).  If no featured image is "
                         "selected above the first image added will become "
                         "the featured image.")
        verbose_name_plural = _("Slideshow (will only display if a featured "
                                "video is not specified above).  If no "
                                "featured image is selected above the first "
                                "image added will become the featured image.")

    def save(self, *args, **kwargs):
        if not self.blog_post.featured_image:
            self.blog_post.featured_image = self.file
            self.blog_post.save()
            if self.id:
               self.delete()
        else:
            super(BlogPostImage, self).save(*args, **kwargs)