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
from django.core.exceptions import ObjectDoesNotExist
from .models import InfoInteres
from Welpe.profile.models import LikeInfo, Comments



utilsForAll = UtilsForAll()


def get_mail_list(event):
    # list of admin of the event to send when we change call for paper
    cc = event.adminlist.replace(";", " ").replace(",", " ").split()
    cc.append(event.owner.email)
    return cc


class InfoUtils:
    def getLikeInfo(self, info, user):
        """
        Esta funcion se encarga de buscar si el usuario ha guardado la info como favorita
        :param info: la ponencia (speech)
        :param usuario: el usuario
        :return: retorna el objeto encontrado o none
        """
        like = None
        if user.is_authenticated():
            try:
                like = LikeInfo.objects.get(info=info, usuario=user)
            except ObjectDoesNotExist, e:
                pass
        return like

    def getLikeCommentInfos(self, user, listado_infos, filtrar_like):
        """
        Esta funcion se encarga de crear una lista con todas las infos y likes (del usuario)
        :param usuario: el usuario
        :return: retorna el objeto encontrado o none
        """
        listado_infos_likes = []
        if filtrar_like:
            for elemento in listado_infos:
                try:
                    LikeInfo.objects.get(info=elemento, usuario=user)
                    info = {}
                    info["info"] = elemento
                    info["like"] = LikeInfo.objects.filter(info=elemento).count()
                    info["comment"]=Comments.objects.filter(page=elemento).count()
                    if not user.is_authenticated():
                        LikeInfo.objects.get(info=elemento, usuario=user)
                        info["likeInfo"] = True
                    else:
                        info["likeInfo"] = False
                    listado_infos_likes.append(info)
                except ObjectDoesNotExist, e:
                    pass
        else:
            for elemento in listado_infos:
                info = {}
                info["info"] = elemento
                info["like"] = LikeInfo.objects.filter(info=elemento).count()
                info["comment"] = Comments.objects.filter(page=elemento).count()
                try:
                    if user.is_authenticated():
                        LikeInfo.objects.get(info=elemento, usuario=user)
                        info["likeInfo"] = True
                    else:
                        info["likeInfo"] = False
                except ObjectDoesNotExist, e:
                    info["likeInfo"] = False
                listado_infos_likes.append(info)
        return listado_infos_likes


    def getInfoByPK(self, pk=None):
        if not pk:
            raise ObjectDoesNotExist()
        try:
            result = InfoInteres.objects.get(pk=pk)
        except ObjectDoesNotExist, e:
            return None
        return result

    def getInfo(self, info):

        try:
            return InfoInteres.objects.get(slug='informacion/' + info, status=CONTENT_STATUS_PUBLISHED)
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


    def getExcelHeader_for_proposals(self, event):
        """
        adaptar
        :param event: The event we export to excel
        :return: The row that will be header of our table
        """
        columns = []
        columns.append((u"Event", 4000))
        columns.append((u"ID/Passport", 4000))
        columns.append((u"Name", 4000))
        columns.append((u"Email", 10000))
        columns.append((u"Company", 4000))
        columns.append((u"Phone.", 4000))
        columns.append((u"Title", 10000))
        columns.append((u"Level.", 4000))
        columns.append((u"Description", 10000))
        columns.append((u"Language", 4000))
        columns.append((u"Type", 4000))
        columns.append((u"Prop. Status", 4000))
        columns.append((u"File", 6000))
        return columns


    def getExcelHeader_for_register(self, event):
        """
        :param event: The event we export to excel
        :return: The row that will be header of our table
        """
        columns = []
        columns.append((u"id", 2000))
        columns.append((u"ID/passport", 4000))
        columns.append((u"Name", 5000))
        columns.append((u"Email", 10000))
        columns.append((u"Phone", 4000))
        columns.append((u"Company", 4000))
        if event.preguntar_profile:
            columns.append((u"Profile", 6000))
        columns.append((u"Worcenter", 4000))
        if event.permitir_solicitar_viaje:
            columns.append((u"Travel", 4000))
        if event.permitir_solicitar_alojamiento:
            columns.append((u"Hotel", 4000))
        if event.preguntar_cena:
            columns.append((u"Dinner", 4000))
        if event.preguntar_alergias:
            columns.append((u"Food indications", 10000))

        return columns


    def getExcelContent_for_register(self, event, participante):
        """
        :param event: The event we want to export participants or waiting list
        :param participante: The registered user or waiting list user
        :return: the row we need to add in Excel
        """
        columns = []
        columns.append(str(participante.id).decode("utf-8"))
        columns.append(participante.documento)
        columns.append(participante.id_usuario.first_name)
        columns.append(participante.id_usuario.email)
        columns.append(participante.telefono)
        columns.append(participante.id_usuario.company)
        if event.preguntar_profile:
            columns.append(participante.main_profile)
        if event.preguntar_workcenter:
            columns.append(participante.workcenter)
        if event.permitir_solicitar_viaje:
            columns.append(participante.solicitaViaje)
        if event.permitir_solicitar_alojamiento:
            columns.append(participante.solicitaHotel)
        if event.preguntar_cena:
            columns.append(participante.preguntar_cena)
        if event.preguntar_alergias:
            columns.append(participante.food_indications)

        return columns


    def getExcelContent_for_proposals(self, event, propuesta):
        """
        :param event: The event we want to export participants or waiting list
        :param participante: The registered user or waiting list user
        :return: the row we need to add in Excel
        """
        site = get_current_site(None).domain

        columns = []
        columns.append(event.title)
        columns.append(propuesta.documento)
        columns.append(propuesta.id_usuario.first_name)
        columns.append(propuesta.id_usuario.email)
        columns.append(propuesta.id_usuario.company)
        columns.append(str(propuesta.telefono).decode("UTF-8"))
        columns.append(propuesta.titulo)
        columns.append(propuesta.level)
        columns.append(propuesta.descripcion)
        columns.append(propuesta.language)
        columns.append(propuesta.type)
        if propuesta.estado_propuesta == 2:
            columns.append("Rejected")
        elif propuesta.estado_propuesta == 1:
            columns.append("Acepted")
        else:
            columns.append("Sent")
        if propuesta.archivo:
            columns.append(site + propuesta.archivo.url)
        else:
            columns.append("")
        return columns

