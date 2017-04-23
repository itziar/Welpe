# coding=utf-8
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.pages.models import Page, RichText
from Welpe.basicModels.models import GenericContent
from mezzanine.utils.sites import current_site_id
from django.contrib.auth.models import User
import os
import shutil
import Welpe.settings



def _get_current_domain():
    return Site.objects.get(id=current_site_id()).domain

def user_directory(propuestas, filename):
    # file will be uploaded to MEDIA_ROOT/eventsProposals/event<event_id>/proposal<proposal_id>/<filename>
    return 'proposals/{0}/{1}'.format(propuestas.pk, filename)

class EstadoPropuesta:
    Enviado, Aceptado, Rechazado = range(3)


class Propuestas(Page, RichText, GenericContent):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo=models.TextField(max_length=150)
    descripcion = RichTextField()
    archivo = models.FileField(upload_to=user_directory, null=True, blank=True)
    estado_propuesta = models.SmallIntegerField(
        choices=(
            (EstadoPropuesta.Enviado, "Enviado"),
            (EstadoPropuesta.Aceptado, "Aceptado"),
            (EstadoPropuesta.Rechazado, "Rechazado"),
        ),
        default=EstadoPropuesta.Enviado, blank=False)

    def delete(self, *args, **kwargs):
        folder=os.path.join(Welpe.settings.MEDIA_ROOT, "proposals")
        folder_proposals=os.path.join(folder, str(self.id))
        try:
            shutil.rmtree(folder_proposals)
        except:
            pass
        super(Propuestas, self).delete(*args, **kwargs)

class CommentsPropuesta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    propuesta = models.ForeignKey(Propuestas, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=150)
    comentario = RichTextField()
    #posibilidad de que el comentario sea anónimo
    anonimo = models.BooleanField(default=False)
    # posibilidad de subir archivos?
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __unicode__(self):
        return u"Comentario %i" % (self.id)