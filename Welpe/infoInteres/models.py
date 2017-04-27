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




def user_directory_informacion(informacion, filename):
    # file will be uploaded to MEDIA_ROOT/informaicon/<informacion_id>/<filename>
    return 'informacion/{0}/{1}'.format(informacion.pk, filename)


class TipoInformacion:
    Beca, Programa, Curso, Concurso, Otros = range(5)


class InfoInteres(Page, RichText, GenericContent):
    # meter un campo que sea practicas o trabajo y otro de requisitos
    descripcion = RichTextField()
    cuando = models.CharField(max_length=150, blank=True)
    donde = models.CharField(max_length=150, blank=True)
    url = models.URLField()
    attached_file = models.FileField(_("Fichero Adjunto"), upload_to=user_directory_informacion, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_informacion = models.SmallIntegerField(
        choices=(
            (TipoInformacion.Beca, "Beca"),
            (TipoInformacion.Programa, "Programa"),
            (TipoInformacion.Curso, "Curso"),
            (TipoInformacion.Concurso, "Concurso"),
            (TipoInformacion.Otros, "Otros"),
        ),
        default=TipoInformacion.Otros, blank=False)

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
        folder = os.path.join(settings.MEDIA_ROOT, "informaicon")
        folder_info = os.path.join(folder, str(self.id))
        try:
            shutil.rmtree(folder_info)
        except:
            pass
        super(InfoInteres, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Información Interesante")
        verbose_name_plural = _("Listado de información interesante")


class CommentsInfo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.ForeignKey(InfoInteres, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=150)
    comentario = RichTextField()
    # posibilidad de que el comentario sea anónimo
    anonimo = models.BooleanField(default=False)
    # posibilidad de subir archivos?
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __unicode__(self):
        return u"Comentario %i" % (self.id)