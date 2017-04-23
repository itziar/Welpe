# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from mezzanine.core.fields import RichTextField
from django.contrib.auth.models import User


class Comments(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.TextField(max_length=150)
    comentario = RichTextField()
    # posibilidad de subir archivos?
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __unicode__(self):
        return u"Comentario %i" % (self.id)
