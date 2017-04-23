# coding=utf-8
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext as _
from mezzanine.core import request
from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.utils.models import upload_to
from mezzanine.utils.sites import current_site_id
from django.contrib.auth.models import User
from Welpe.basicModels.models import GenericContent
import os
import shutil
from Welpe import settings




def _get_current_domain():
    return Site.objects.get(id=current_site_id()).domain

def user_directory_miniactividades(miniactividad, filename):
    # file will be uploaded to MEDIA_ROOT/actividad/actividad<actividad_id>/miniactividad<miniactividad_id>/<filename>
    return 'actividad/{0}/miniactividad/{1}/{2}'.format(miniactividad.actividad.pk, miniactividad.pk, filename)

def user_directory_actividades(actividad, filename):
    return 'actividad/{0}/{1}'.format(actividad.pk, filename)


class Actividades(Page, RichText, GenericContent):
    # fechas y horas del evento (inicio y fin)
    start_date = models.DateField()
    finish_date = models.DateField()
    destacado = models.BooleanField(_("Es una actividad destacada"), default=False)
    url = models.TextField(max_length=500, default="", blank=True)
    descripcion = RichTextField()
    # para los participantes
    limite_participantes = models.BooleanField(_("limit participants"), default=False)
    limit = models.IntegerField(blank=True, null=True)
    # localizacion
    lugar = models.TextField(max_length=500, blank=True)
    # creditos de libre eleccion
    creditos_rac=models.BooleanField(_("Se conceden RAC"), default=False)
    n_rac=models.IntegerField(blank=True, null=True)

    adminlist = models.TextField(max_length=500, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # inscripciones al evento
    permitir_inscriptions = models.BooleanField(_("Permitir inscripciones"), default=False)
    fecha_inscripcion_inicio = models.DateField(blank=True, null=True)
    fecha_inscripcion_final = models.DateField(blank=True, null=True)
    lista_espera = models.BooleanField(_("Permitir lista de espera"), default=False)

    enviar_notificaciones = models.BooleanField(_("Enviar notificaciones"), default=True)
    email_organizador = models.EmailField(_("Email to receive notifications"), null=True, blank=True)
    attached_file = models.FileField(_("Attach an file"), upload_to=user_directory_actividades, null=True, blank=True)
    incluir_miniactividades=models.BooleanField(_("Incluir MiniActividades"), default=True)

    def has_permissions(self, user):
        """
        Esta funcion comprueba si un usuario tiene permisos sobre el seminario o no
        :param user: usuario
        :return: boleano resultado de la comprobacion de si el user tiene permisos sobre el seminario o no
        """
        if user.is_superuser or (user == self.owner) or (user.email in self.adminlist):
            return True
        return False

    def delete(self, *args, **kwargs):
        # construimos el path del seminario para borrar el posible fichero
        folder = os.path.join(settings.MEDIA_ROOT, "actividad")
        folder_event = os.path.join(folder, str(self.id))
        try:
            shutil.rmtree(folder_event)
        except:
            pass
        super(Actividades, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Actividades")
        verbose_name_plural = _("Lista de Actividades")
        ordering = ("-start_date",)


class UsuariosRegistradosActividades(models.Model):
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s (%s)' % (self.usuario.first_name, self.actividad.title)


class UsuariosListaEsperaActividades(models.Model):
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class MiniActividad(models.Model):
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=510, blank=False, null=False)
    descripcion = RichTextField(blank=True)
    archivo = models.FileField(upload_to=user_directory_miniactividades, null=True, blank=True)
    place = models.CharField(max_length=500, blank=True)
    fecha = models.TextField(max_length=500, blank=True)
    hora = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = _("Mini-actividad")
        verbose_name_plural = _("Lista de mini-actividades")

    def __unicode__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        # construimos el path
        folder = os.path.join(settings.MEDIA_ROOT, "actividades")
        folder_event = os.path.join(folder, str(self.actividad.id))
        folder = os.path.join(folder_event, "miniactividad")
        folder_speech = os.path.join(folder, str(self.id))
        try:
            shutil.rmtree(folder_speech)
        except:
            pass
        super(MiniActividad, self).delete(*args, **kwargs)


class OrganizadorMiniActividad(models.Model): #organizador
    miniactividad = models.ForeignKey(MiniActividad, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    bio = RichTextField(blank=True)
    email=models.EmailField(blank=True)
    company = models.CharField(max_length=255, blank=True)
    photo = FileField(verbose_name=_("Photo"),
                      upload_to=upload_to("contentImg", "miniactividad_autor"),
                      format="Image", max_length=255, null=True, blank=True)

    def delete(self, *args, **kwargs):
        try:
            self.photo.delete()
        except:
            pass
        super(MiniActividad, self).delete(*args, **kwargs)

#preregistro
class AsistentesMiniActividad(models.Model):
    miniactividad = models.ForeignKey(MiniActividad, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)




class CommentsActividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=150)
    comentario = RichTextField()
    # posibilidad de subir archivos?
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __unicode__(self):
        return u"Comentario %i" % (self.id)


class CommentsMiniActividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    miniactividad = models.ForeignKey(MiniActividad, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=150)
    comentario = RichTextField()
    # posibilidad de subir archivos?
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __unicode__(self):
        return u"Comentario %i" % (self.id)
