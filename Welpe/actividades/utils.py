from __future__ import unicode_literals

import Welpe.settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, Http404
from django.template import Context
from django.template.loader import get_template
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from datetime import date
from .models import UsuariosRegistradosActividades, Actividades, CommentsActividad
from django.contrib.sites.shortcuts import get_current_site
from Welpe.site_utils import UtilsForAll
from Welpe.profile.models import LikeActividad

utilsForAll = UtilsForAll()


def get_mail_list(actividad):
    # lista de administradores a quien redirigir el correo de la actividad
    cc = actividad.adminlist.replace(";", " ").replace(",", " ").split()
    cc.append(actividad.owner.email)
    return cc


class ActividadesUtils:
    def comparar_fechas_inicio(self, today, fecha_inicio):
        """
        Esta funcion compara la fecha de inicio con la de hoy
        :param today: fecha de hoy
        :param fecha_inicio: fecha de inicio
        :return: True si hoy es menor que fecha_inicio y False al contrario
        """
        if not fecha_inicio:
            raise Exception("Fecha Inicio cant be None")
        return today < fecha_inicio

    def comparar_fechas_final(self, today, fecha_final):
        """
         Esta funcion compara la fecha final con la de hoy
        :param today: fecha de hoy
        :param fecha_final: fecha final
        :return: True si hoy es mayor que fecha_final y False al contrario
        """
        if not fecha_final:
            raise Exception("Fecha Final cant be None")
        return today > fecha_final

    def getActividadByPK(self, pk=None):
        if not pk:
            raise ObjectDoesNotExist()
        try:
            result = Actividades.objects.get(pk=pk)
        except ObjectDoesNotExist, e:
            return None
        return result

    def getLikeCommentActividades(self, user, listado_act, filtrar_like):
        """
        Esta funcion se encarga de crear una lista con todas las actividades y likes (del usuario)
        :param usuario: el usuario
        :return: retorna el objeto encontrado o none
        """
        listado_act_likes = []
        if filtrar_like:
            for elemento in listado_act:
                try:
                    actividad = {}
                    actividad["actividad"] = elemento
                    actividad["like"] = LikeActividad.objects.filter(actividad=elemento).count()
                    actividad["comment"] = CommentsActividad.objects.filter(actividad=elemento).count()
                    if user.is_authenticated():
                        LikeActividad.objects.get(actividad=elemento, usuario=user)
                        actividad["likeAct"] = True
                    else:
                        actividad["likeAct"] = False
                    listado_act_likes.append(actividad)
                except ObjectDoesNotExist, e:
                    pass
        else:
            for elemento in listado_act:
                actividad = {}
                actividad["actividad"] = elemento
                actividad["like"] = LikeActividad.objects.filter(actividad=elemento).count()
                actividad["comment"] = CommentsActividad.objects.filter(actividad=elemento).count()
                try:
                    if user.is_authenticated():
                        LikeActividad.objects.get(actividad=elemento, usuario=user)
                        actividad["likeAct"] = True
                    else:
                        actividad["likeAct"] = False
                except ObjectDoesNotExist, e:
                    actividad["likeAct"] = False
                listado_act_likes.append(actividad)
        return listado_act_likes

    def getLikeActividad(self, actividad, user):
        """
        Esta funcion se encarga de buscar si el usuario ha guardado la oferta como favorita
        :param oferta: la ponencia (speech)
        :param usuario: el usuario
        :return: retorna el objeto encontrado o none
        """
        like = None
        if user.is_authenticated():
            try:
                like = LikeActividad.objects.get(actividad=actividad, usuario=user)
            except ObjectDoesNotExist, e:
                pass
        return like

    def getActividad(self, actividad):
        """
        Con esta funcion obtenemos el actividad que estamos buscando
        :param actividad: actividad a buscar en nuestra bbdd
        :return: retornamos el actividad o errores (de no encontrado o permisos denegados)
        """
        try:
            return Actividades.objects.get(slug='actividades/' + actividad, status=CONTENT_STATUS_PUBLISHED)
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


    def getExcelHeader_for_register(self, event):
        """
        :param event: The event we export to excel
        :return: The row that will be header of our table
        """
        columns = []
        columns.append((u"id", 2000))
        columns.append((u"Name", 5000))
        columns.append((u"Email", 10000))
        return columns

    def getExcelContent_for_register(self, participante):
        """
        :param event: The event we want to export participants or waiting list
        :param participante: The registered user or waiting list user
        :return: the row we need to add in Excel
        """
        columns = []
        columns.append(str(participante.id).decode("utf-8"))
        columns.append(participante.usuario.first_name)
        columns.append(participante.usuario.email)
        return columns

    def has_permission_registration(self, actividad, user):
        # comparar fechas para ver que estan dentro del periodo de registro
        today = date.today()
        # hay actividad que no tienen fecha de inicio y final
        if actividad.fecha_inscripcion_inicio:
            comparar_inicio = self.comparar_fechas_inicio(today, actividad.fecha_inscripcion_inicio)
        else:
            comparar_inicio = False
        if actividad.start_date:
            comparar_final = self.comparar_fechas_final(today, actividad.start_date)
        else:
            comparar_final = False
        if not comparar_inicio and not comparar_final or actividad.has_permissions(user):
            return True
        else:
            return False
