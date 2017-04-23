# coding=utf-8

from __future__ import unicode_literals

# Create your views here.
# Import models
import os
from mezzanine.pages.models import Page
from django.contrib.auth.decorators import *
from .models import InfoInteres, CommentsInfo
from Welpe.profile.models import LikeInfo
# Import django global objects
from django.shortcuts import redirect
# Import utils and mezzanine objects
from mezzanine.utils.views import TemplateResponse, paginate
from mezzanine.conf import settings
from datetime import date
from django.http import JsonResponse
from Welpe.infoInteres.utils import InfoUtils
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q




utils = InfoUtils()

def clear_filter(request):
    '''
    Esta funcion elimina los filtros aplicados
    :param request: request-post(en un principio) request-gest(por si ponen la url)
    :return: redirect a list_ofertas
    '''
    return redirect(list_infos)


def list_infos(request, template="/pages/info_list.html"):
    listado_infos = InfoInteres.objects.published()
    filtrar_like=False
    if request.method=="POST":
        content = request.POST['content']
        if content != '':
            listado_infos = listado_infos.filter(Q(title__icontains=content) | Q(descripcion__icontains=content))
        # todo sacar el resto de parametros
        tipo_info = request.POST['tipo_info']
        if tipo_info != '':
            listado_infos = listado_infos.filter(tipo_info=tipo_info)
        try:
            like = request.POST['like']
            if like:
                filtrar_like = True
        except:
            pass
    templates = []
    templates.append(u'pages/info_list.html')
    # context = {"lista": lista, "most_viewed_talks":most_viewed_talks, "most_rated_talks":most_rated_talks}
    listado_infos = utils.getLikeCommentInfos(request.user, listado_infos, filtrar_like)
    context = {"lista": listado_infos}
    templates.append(template)
    return TemplateResponse(request, templates, context)



def view_info(request, info=None, template="pages/info.html"):
    info = utils.getInfo(info)
    today = date.today()
    like = utils.getLikeInfo(info, request.user)
    number_of_likes = LikeInfo.objects.filter(info=info).count()
    comments = CommentsInfo.objects.filter(info=info)
    context = {"info": info,
               "today": today,
               "likeInfo": like,
               "comments": comments,
               "number_of_likes": number_of_likes
               }
    templates = []
    templates.append(u'pages/info.html')
    templates.append(template)
    return TemplateResponse(request, templates, context)


@login_required
def add_comment(request, info):
    """Devuelve la pagina del foro y almacena comentarios nuevos"""
    info = utils.getInfo(info)
    if request.method == "POST":
        titulo = utils.getfromPost(request, "title")
        comentario=utils.getfromPost(request, "comentario")
        new_comment = CommentsInfo(titulo=titulo, comentario=comentario, info=info, usuario=request.user)
        new_comment.save()
    return redirect(info)


@login_required
def like_info(request, info=None):
    info = utils.getInfo(info)
    if request.POST:
        guardado = utils.getLikeInfo(info, request.user)
        if guardado:
            guardado.delete()
            return JsonResponse({'status': 'unliked',
                                 'number_of_likes': LikeInfo.objects.filter(info=info).count()})
        else:
            # guargar el preregistro
            new_like = LikeInfo(info=info, usuario=request.user)
            new_like.save()
            return JsonResponse({'status': 'like',
                                 'number_of_likes': LikeInfo.objects.filter(info=info).count()})
        return JsonResponse({'status': 'error'})


@login_required
def add_info(request):
    if not request.POST:
        return redirect("home_info")
    # get the father
    parent = Page.objects.get_by_natural_key("informacion")
    # saco los campos del formulario
    pk = utils.getfromPost(request, 'pk')
    title = utils.getfromPost(request, 'title')
    descripcion = utils.getfromPost(request, 'descripcion')
    cuando = utils.getfromPost(request, 'cuando')
    donde = utils.getfromPost(request, 'donde')
    url = utils.getfromPost(request, 'url')

    tipo_info = request.POST['tipo_info']
    if tipo_info == 'Beca':
        tipo_info = 0
    elif tipo_info == 'Programa':
        tipo_info = 1
    elif tipo_info == 'Curso':
        tipo_info = 2
    elif tipo_info == 'Concurso':
        tipo_info = 3
    elif tipo_info == 'Otros':
        tipo_info = 4
    delete_file = utils.getfromPost(request, "delete_file")
    attached_file = utils.getfilefromPost(request, 'archivo')
    if attached_file == "/static/media/":
        attached_file = ""
    try:
        info = utils.getInfoByPK(pk)
    except ObjectDoesNotExist, e:
        info = None
    unlinkarchivo = False
    if delete_file:
        unlinkarchivo = True
        if info:
            cola, fichero = os.path.split(info.attached_file.path)
            info.attached_file.delete()
    if info and attached_file:
        if info.attached_file:
            cola, fichero = os.path.split(info.attached_file.path)
            info.attached_file.delete()
    if unlinkarchivo and not attached_file:
        attached_file = ""
    # TODO: cambiar espacios por guiones
    if info:
        info.title = title.decode('utf-8')
        info.descripcion = descripcion
        info.url = url
        info.cuando = cuando
        info.donde = donde
        info.owner = request.user
        info.tipo_informacion = tipo_info
        info.attached_file = attached_file
        info.slug = "informacion/" + unicode(title, "utf-8")  # si cambia el titulo quiero que cambie el slug
    else:
        info = InfoInteres(
            title=title,
            descripcion=descripcion,
            url=url,
            cuando=cuando,
            donde=donde,
            owner=request.user,
            tipo_informacion=tipo_info,
            parent=parent,
            slug="informacion/" + unicode(title, "utf-8"),
            attached_file=""
        )
        # guardamos antes para que el evento tenga id
        info.save()
        info.attached_file = attached_file
    info.save()
    return redirect(info)


@login_required
def delete_info(request):
    """
    Delete the event received as parameter via Form
    :param request: The request
    :return: redirect to /events
    """
    if request.POST:
        pk = utils.getfromPost(request, "pk")
        if pk:
            info = utils.getInfoByPK(pk=pk)
        else:
            raise Exception("Cant delete this event")
        info.delete()
    return redirect("home_info")

