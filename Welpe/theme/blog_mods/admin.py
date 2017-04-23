
from copy import deepcopy

from blog.admin import BlogPostAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import TabularDynamicInlineAdmin

from models import BlogPostImage

if settings.BLOG_USE_FEATURED_IMAGE:
    class BlogPostImageInline(TabularDynamicInlineAdmin):
        model = BlogPostImage


    # monkey patch featured_video onto BlogPost
    custom_blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
    BlogPostAdmin.fieldsets = custom_blog_fieldsets
    BlogPostAdmin.inlines = (BlogPostImageInline,)
