# coding=utf-8

from __future__ import unicode_literals
# Create your views here.
# Import models
import os
from mezzanine.pages.models import Page
from django.contrib.auth.decorators import *
from .models import Propuestas, CommentsPropuesta
from Welpe.profile.models import LikePropuesta
# Import django global objects
from django.shortcuts import redirect
# Import utils and mezzanine objects
from mezzanine.utils.views import TemplateResponse, paginate
from mezzanine.conf import settings
from datetime import date
from django.http import JsonResponse
from Welpe.propuestas.utils import PropuestasUtils
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from Welpe.manageUser.views import User

utils = PropuestasUtils()


def clear_filter(request):
    '''
    Esta funcion elimina los filtros aplicados
    :param request: request-post(en un principio) request-gest(por si ponen la url)
    :return: redirect a list_ofertas
    '''
    return redirect(list_propuesta)


def list_propuesta(request, template="/pages/propuesta_list.html"):
    """
    Esta funcion devuelve una lista de todos los eventos, ordenados por destacados y luego por fecha de inicio
    :param request: request-get
    :param template: events_list
    :return: template(events_list) rellenado con los eventos
    """
    listado_propuestas = Propuestas.objects.all()
    filtrar_like = False
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            listado_propuestas = listado_propuestas.filter(
                Q(title__icontains=content) | Q(descripcion__icontains=content))
        # todo sacar el resto de parametros
        estado_propuesta = request.POST['estado_propuesta']
        if estado_propuesta != '':
            if estado_propuesta == 'Enviado':
                estado_propuesta = 0
            elif estado_propuesta == 'Aceptado':
                estado_propuesta = 1
            elif estado_propuesta == 'Rechazado':
                estado_propuesta = 2
            listado_propuestas = listado_propuestas.filter(estado_propuesta=estado_propuesta)
        try:
            like = request.POST['like']
            if like:
                filtrar_like = True
        except:
            pass
    templates = []
    templates.append(u'pages/propuesta_list.html')
    # context = {"lista": lista, "most_viewed_talks":most_viewed_talks, "most_rated_talks":most_rated_talks}
    listado_propuestas = utils.getLikeCommentPropuestas(request.user, listado_propuestas, filtrar_like)
    context = {"lista": listado_propuestas}
    templates.append(template)
    return TemplateResponse(request, templates, context)


def view_propuesta(request, propuesta=None, template="pages/propuesta.html"):
    """
    Esta funcion te muestra la oferta seleccionada
    :param request: reques-get
    :param info: oferta seleccionada
    :param template: events
    :return: template(events) rellenado con los datos del evento seleccionado
    """
    propuesta = utils.getPropuesta(propuesta)

    today = date.today()
    like = utils.getLikePropuesta(propuesta, request.user)
    number_of_likes = LikePropuesta.objects.filter(propuesta=propuesta).count()
    comments = CommentsPropuesta.objects.filter(propuesta=propuesta)
    context = {"propuesta": propuesta,
               "today": today,
               "likeInfo": like,
               "comments": comments,
               "number_of_likes": number_of_likes
               }
    templates = []
    templates.append(u'pages/propuesta.html')
    templates.append(template)
    return TemplateResponse(request, templates, context)


@login_required
def add_comment(request, propuesta):
    """Devuelve la pagina del foro y almacena comentarios nuevos"""
    propuesta = utils.getPropuesta(propuesta)
    if request.method == "POST":
        try:
            existe = request.POST['anonimo']
            anonimo = True
        except:
            anonimo = False
        titulo = utils.getfromPost(request, "title")
        comentario = utils.getfromPost(request, "comentario")
        new_comment = CommentsPropuesta(titulo=titulo, comentario=comentario, propuesta=propuesta, usuario=request.user,
                                        anonimo=anonimo)
        new_comment.save()
    return redirect(propuesta)


@login_required
def like_propuesta(request, propuesta=None):
    """
    Esta funcion es para saber el numero de usuarios registrados a un evento que van a asistir a una ponencia
    :param request: el request para sacar los datos
    :param info: el evento donde se encuentra la ponencia
    :return: retorna un json que cuenta el numero de users preregistrados y los muestra
    """

    propuesta = utils.getPropuesta(propuesta)
    if request.POST:
        guardado = utils.getLikePropuesta(propuesta, request.user)
        if guardado:
            guardado.delete()
            return JsonResponse({'status': 'unliked',
                                 'number_of_likes': LikePropuesta.objects.filter(propuesta=propuesta).count()})
        else:
            # guargar el preregistro
            new_like = LikePropuesta(propuesta=propuesta, usuario=request.user)
            new_like.save()
            return JsonResponse({'status': 'like',
                                 'number_of_likes': LikePropuesta.objects.filter(propuesta=propuesta).count()})
        return JsonResponse({'status': 'error'})


@login_required
def add_propuesta(request):
    """
    Esta funcion crea o modifica un nuevo evento
    :param request: el request
    :return: retorna a la pagina principal del evento creado o modificado
    """
    if not request.POST:
        return redirect("home_propuestas")
    # get the father

    # saco los campos del formulario
    pk = utils.getfromPost(request, 'pk')
    title = utils.getfromPost(request, 'title')
    descripcion = utils.getfromPost(request, 'descripcion')
    parent = Page.objects.get_by_natural_key("propuestas")
    try:
        estado_propuesta = request.POST['estado_propuesta']
    except:
        estado_propuesta = 'Enviado'
    if estado_propuesta == 'Enviado':
        estado_propuesta = 0
    elif estado_propuesta == 'Aceptado':
        estado_propuesta = 1
    elif estado_propuesta == 'Rechazado':
        estado_propuesta = 2

    id_usuario = utils.getfromPost(request, "id_usuario")
    if id_usuario:
        user = User.objects.get(id=id_usuario)
    else:
        user = request.user
    delete_file = utils.getfromPost(request, "delete_file")
    attached_file = utils.getfilefromPost(request, 'archivo')
    if attached_file == "/static/media/":
        attached_file = ""
    try:
        propuesta = utils.getPropuestaByPK(pk)
    except ObjectDoesNotExist, e:
        propuesta = None
    unlinkarchivo = False
    if delete_file:
        unlinkarchivo = True
        if propuesta:
            cola, fichero = os.path.split(propuesta.attached_file.path)
            propuesta.attached_file.delete()
    if propuesta and attached_file:
        if propuesta.attached_file:
            cola, fichero = os.path.split(propuesta.attached_file.path)
            propuesta.attached_file.delete()
    if unlinkarchivo and not attached_file:
        attached_file = ""
    # TODO: cambiar espacios por guiones
    if propuesta:
        propuesta.title = title.decode('utf-8')
        propuesta.descripcion = descripcion
        propuesta.usuario = user
        propuesta.estado_propuesta = estado_propuesta
        propuesta.archivo = attached_file

    else:
        propuesta = Propuestas(
            title=title.decode('utf-8'),
            descripcion=descripcion,
            usuario=user,
            estado_propuesta=estado_propuesta,
            archivo=attached_file,
            parent=parent,
        )
        # guardamos antes para que el evento tenga id
        propuesta.save()
        propuesta.attached_file = attached_file
    propuesta.save()
    return redirect(propuesta)


@login_required
def delete_propuesta(request):
    """
    Delete the event received as parameter via Form
    :param request: The request
    :return: redirect to /events
    """
    if request.POST:
        pk = utils.getfromPost(request, "pk")
        if pk:
            propuesta = utils.getPropuestaByPK(pk=pk)
        else:
            raise Exception("Cant delete this event")
        propuesta.delete()
    return redirect(view_propuesta)


@login_required
def estado(request, propuesta=None):
    """
    Esta funcion cambia el estado de una propuesta
    :param request: el request
    :param event: el evento
    :return: retorna a la pagina principal del evento
    """
    propuesta = utils.getPropuesta(propuesta)
    #TODO permissions
    if not propuesta.has_permissions(request.user):
        return HttpResponseForbidden()

    if request.POST:
        pk = request.POST['pk']
        id_usuario = request.POST['id_usuario']
        status = request.POST['estado_propuesta']
        if status == 'Sent':
            estado = 0
        elif status == 'Accepted':
            estado = 1
        elif status == 'Rejected':
            estado = 2

        user = utils.getUserInfoId(id_usuario)
        if not user:
            raise Exception("Cant find user")
        #todo
        propuesta = utils.getPropuestaUsuario(propuesta, pk, user)

        propuesta.estado_propuesta = estado
        propuesta.save()
