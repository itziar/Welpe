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


def user_directory_profile(usuario, filename):
    # file will be uploaded to MEDIA_ROOT/profile/<user_id>/<filename>
    return 'profile/{0}/{1}'.format(usuario.pk, filename)


class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    dni = models.TextField(max_length=15, blank=True)
    bio = RichTextField()
    location = models.CharField(max_length=30, blank=True)
    show_email = models.BooleanField(default=False,
                                     verbose_name='mostrar email')
    photo = models.FileField(_("Imagen"), upload_to=user_directory_profile, null=True, blank=True)
    telefono = models.TextField(max_length=15)
    pagina_web = models.URLField()
    # para profesor
    departamento = models.TextField(max_length=150)
    puesto = models.TextField(max_length=150)
    formacion = models.TextField(max_length=150)
    investigacion = models.TextField(max_length=150)
    # para alumnos
    grado = models.TextField(max_length=150, blank=True)
    curso = models.IntegerField()

    def delete(self, *args, **kwargs):
        try:
            self.photo.delete()
        except:
            pass
        super(Profile, self).delete(*args, **kwargs)



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
