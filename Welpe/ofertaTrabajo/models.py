# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext as _
from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField
from Welpe.basicModels.models import GenericContent
from django.contrib.auth.models import User

import os
import shutil
from Welpe import settings



def user_directory_ofertas(oferta, filename):
    # file will be uploaded to MEDIA_ROOT/ofertaTrabajo/<oferta_id>/<filename>
    return 'ofertaTrabajo/{0}/{1}'.format(oferta.pk, filename)


class TipoContrato:
    Beca, Indefinido, Otros = range(3)


class OfertaTrabajo(Page, RichText, GenericContent):
    # meter un campo que sea practicas o trabajo y otro de requisitos
    descripcion = RichTextField()
    como_aplicar = RichTextField()
    cuando = models.CharField(max_length=150, blank=True)
    donde = models.CharField(max_length=150, blank=True)
    url = models.URLField()
    salario = models.CharField(max_length=150, blank=True)
    attached_file = models.FileField(_("Fichero Adjunto"), upload_to=user_directory_ofertas, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_contrato = models.SmallIntegerField(
        choices=(
            (TipoContrato.Beca, "Prácticas"),
            (TipoContrato.Indefinido, "Indefinido"),
            (TipoContrato.Otros, "Otros"),
        ),
        default=TipoContrato.Otros, blank=False)

    def has_permissions(self, user):
        '''
        This function checks if an user has permissions to do something with an offers
        :param user:
        :return: value of comparation
        '''
        if user.is_superuser or (user == self.owner):
            return True
        return False

    def delete(self, *args, **kwargs):
        # construimos el path del evento
        folder = os.path.join(settings.MEDIA_ROOT, "ofertaTrabajo")
        folder_event = os.path.join(folder, str(self.id))
        try:
            shutil.rmtree(folder_event)
        except:
            pass
        super(OfertaTrabajo, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Oferta")
        verbose_name_plural = _("Listado de Ofertas")
