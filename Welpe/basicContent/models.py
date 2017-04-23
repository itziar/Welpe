from django.db import models

# Create your models here.
from mezzanine.pages.models import Page, RichText
from Welpe.basicModels.models import GenericContent
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class BasicContent(Page, RichText, GenericContent):
    pass


class ExternalLink(models.Model):
    externalLink = models.ForeignKey(BasicContent, on_delete=models.CASCADE, related_name="ext_links")
    url = models.URLField(max_length=500)
    nameToShow = models.CharField(max_length=500)


class AttachedFile(models.Model):
    attachedFile = models.ForeignKey(BasicContent, on_delete=models.CASCADE, related_name="att_files")
    fileName = models.FileField(upload_to="contentFiles")
    fileSummary = models.CharField(max_length=500)

    def delete(self, *args, **kwargs):
        self.fileName.delete()
        super(AttachedFile, self).delete(*args, **kwargs)


@receiver(pre_delete, sender=AttachedFile)
def attachedFile_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.fileName.delete(False)