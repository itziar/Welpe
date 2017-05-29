# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext as _
from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page, RichText

from Welpe.actividades.models import Actividades
from Welpe.infoInteres.models import InfoInteres
from Welpe.ofertaTrabajo.models import OfertaTrabajo
from Welpe.propuestas.models import Propuestas
from django.contrib.sites.models import Site
from mezzanine.pages.models import Page, RichText
from mezzanine.utils.sites import current_site_id
from django.contrib.auth.models import User
from Welpe.basicModels.models import GenericContent
import os
import shutil
from Welpe import settings


def _get_current_domain():
    return Site.objects.get(id=current_site_id()).domain


def user_directory_profile(usuario, filename):
    # file will be uploaded to MEDIA_ROOT/profile/<user_id>/<filename>
    return 'profile/{0}/{1}'.format(usuario.pk, filename)


def user_directory_comments(page, filename):
    return 'comments/{0}/{1}'.format(page.pk, filename)


class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    dni = models.CharField(max_length=15, blank=True)
    bio = RichTextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    photo = models.FileField(_("Imagen"), upload_to=user_directory_profile, null=True, blank=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    pagina_web = models.URLField(null=True, blank=True)
    def delete(self, *args, **kwargs):
        try:
            self.photo.delete()
        except:
            pass
        super(Profile, self).delete(*args, **kwargs)

class ProfileProfesor(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    # para profesor
    departamento = models.TextField(max_length=150, blank=True)
    puesto = models.TextField(max_length=150, blank=True)
    formacion = models.TextField(max_length=150, blank=True)
    investigacion = models.TextField(max_length=150, blank=True)

class ProfileAlumno(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    # para alumnos
    grado = models.TextField(max_length=150, blank=True)
    curso = models.IntegerField(null=True, blank=True)




class LikeOferta(models.Model):
    oferta = models.ForeignKey(OfertaTrabajo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class LikeInfo(models.Model):
    info = models.ForeignKey(InfoInteres, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class LikeActividad(models.Model):
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class LikePropuesta(models.Model):
    propuesta = models.ForeignKey(Propuestas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinatario')
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remitente')
    subject = models.TextField(max_length=150, blank=True)
    body = RichTextField()
    date = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=150)
    comentario = RichTextField()
    # posibilidad de que el comentario sea anónimo
    anonimo = models.BooleanField(default=False)
    # posibilidad de subir archivos
    archivo = models.FileField(upload_to=user_directory_comments, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __unicode__(self):
        return u"Comentario %i" % self.id

    def delete(self, *args, **kwargs):
        # construimos el path del seminario para borrar el posible fichero
        folder = os.path.join(settings.MEDIA_ROOT, "comments")
        folder_event = os.path.join(folder, str(self.id))
        try:
            shutil.rmtree(folder_event)
        except:
            pass
        super(Comments, self).delete(*args, **kwargs)
