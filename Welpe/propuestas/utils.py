from __future__ import unicode_literals

import Welpe.settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, Http404
from django.template import Context
from django.template.loader import get_template
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from datetime import date
from Welpe.site_utils import UtilsForAll


from django.contrib.sites.shortcuts import get_current_site
from .models import Propuestas, CommentsPropuesta
from Welpe.profile.models import LikePropuesta

from Welpe.manageUser.views import User

utilsForAll = UtilsForAll()


def get_mail_list(event):
    # list of admin of the event to send when we change call for paper
    cc = event.adminlist.replace(";", " ").replace(",", " ").split()
    cc.append(event.owner.email)
    return cc


class PropuestasUtils:
    def getLikePropuesta(self, propuesta, user):
        """
        Esta funcion se encarga de buscar si el usuario ha guardado la oferta como favorita
        :param oferta: la ponencia (speech)
        :param usuario: el usuario
        :return: retorna el objeto encontrado o none
        """
        like = None
        if user.is_authenticated():
            try:
                like = LikePropuesta.objects.get(propuesta=propuesta, usuario=user)
            except ObjectDoesNotExist, e:
                pass
        return like

    def getLikeCommentPropuestas(self, user, listado_propuestas, filtrar_like):
        """
        Esta funcion se encarga de crear una lista con todas las ofertas y likes (del usuario)
        :param usuario: el usuario
        :return: retorna el objeto encontrado o none
        """
        listado_propuestas_likes = []
        if filtrar_like:
            for elemento in listado_propuestas:
                try:
                    propuesta = {}
                    propuesta["propuesta"] = elemento
                    propuesta["like"] = LikePropuesta.objects.filter(propuesta=elemento).count()
                    propuesta["comment"] = CommentsPropuesta.objects.filter(propuesta=elemento).count()
                    if user.is_authenticated():
                        LikePropuesta.objects.get(propuesta=elemento, usuario=user)
                        propuesta["likePropuesta"] = True
                    else:
                        propuesta["likePropuesta"] = False
                    listado_propuestas_likes.append(propuesta)
                except ObjectDoesNotExist, e:
                    pass
        else:
            for elemento in listado_propuestas:
                propuesta = {}
                propuesta["propuesta"] = elemento
                propuesta["like"] = LikePropuesta.objects.filter(propuesta=elemento).count()
                propuesta["comment"] = CommentsPropuesta.objects.filter(propuesta=elemento).count()
                try:
                    if user.is_authenticated():
                        LikePropuesta.objects.get(propuesta=elemento, usuario=user)
                        propuesta["likePropuesta"] = True
                    else:
                        propuesta["likePropuesta"] = False
                except ObjectDoesNotExist, e:
                    propuesta["likePropuesta"] = False
                listado_propuestas_likes.append(propuesta)
        return listado_propuestas_likes


    def getPropuestaByPK(self, pk=None):
        if not pk:
            raise ObjectDoesNotExist()
        try:
            result = Propuestas.objects.get(pk=pk)
        except ObjectDoesNotExist, e:
            return None
        return result

    def getPropuesta(self, propuesta):
        """
        Con esta funcion obtenemos el evento que estamos buscando
        :param event: evento a buscar en nuestra bbdd
        :return: retornamos el evento o errores (de no encontrado o permisos denegados)
        """
        try:
            return Propuestas.objects.get(slug='propuestas/' + propuesta, status=CONTENT_STATUS_PUBLISHED)
        except PermissionDenied:
            return HttpResponseForbidden()
        except ObjectDoesNotExist:
            raise Http404()


    def getfromPost(self, request, campo=None):
        """Given a field return its value if exists. Return an empty string otherwise."""
        return utilsForAll.getfromPost(request, campo)

    def getfilefromPost(self, request, campo=None):
        """Given a field return its file value if exists. Return an empty string otherwise."""
        return utilsForAll.getfilefromPost(request, campo)

    def getPropuestaUsuario(self, event, pk, user):
        """
        Esta funcion busca una propuesta determinada
        :param event: el evento
        :param pk: id de la propuesta a buscar
        :param user: usuario
        :return: retorna el objeto encontrado o none
        """
        listado_propuestas = None
        try:
            if event.has_permissions(user) and pk:
                listado_propuestas = Propuestas.objects.get(pk=pk)
            else:
                if pk:
                    listado_propuestas = Propuestas.objects.get(id_usuario=user, pk=pk)
        except ObjectDoesNotExist, e:
            pass
        return listado_propuestas


    def getExcelHeader_for_proposals(self, propuesta):
        """
        adaptar
        :param event: The event we export to excel
        :return: The row that will be header of our table
        """
        columns = []
        columns.append((u"DNI/NIE", 4000))
        columns.append((u"Nombre", 4000))
        columns.append((u"Apellidos", 4000))
        columns.append((u"Email", 10000))
        columns.append((u"Curso", 10000))
        columns.append((u"Titulacion", 10000))
        columns.append((u"Titulo", 10000))
        columns.append((u"Descricion", 10000))
        columns.append((u"Estado de la propuesta", 4000))
        columns.append((u"File", 6000))
        return columns


    def getExcelContent_for_proposals(self, propuesta):
        """
        :param event: The event we want to export participants or waiting list
        :param participante: The registered user or waiting list user
        :return: the row we need to add in Excel
        """
        site = get_current_site(None).domain

        columns = []

        columns.append(propuesta.dni)
        columns.append(propuesta.usuario.first_name)
        columns.append(propuesta.usuario.last_name)
        columns.append(propuesta.usuario.email)
        columns.append(propuesta.usuario.curso)
        columns.append(propuesta.usuario.titulacion)
        columns.append(propuesta.title)
        columns.append(propuesta.descripcion)
        if propuesta.estado_propuesta == 2:
            columns.append("Rechazado")
        elif propuesta.estado_propuesta == 1:
            columns.append("Acteptado")
        else:
            columns.append("Enviado")
        if propuesta.archivo:
            columns.append(site + propuesta.archivo.url)
        else:
            columns.append("")
        return columns



    def getUserInfoId(self, id):
        """
        :param id: id usuario
        :return: object user or none
        """
        user = None
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist, e:
            pass
        return user