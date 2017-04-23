# coding=utf-8
from __future__ import unicode_literals

# Create your views here.
# Import models
import os
from mezzanine.pages.models import Page
from django.contrib.auth.decorators import *
from .models import OfertaTrabajo, CommentsOferta
from Welpe.profile.models import LikeOferta
# Import django global objects
from django.shortcuts import redirect
# Import utils and mezzanine objects
from mezzanine.utils.views import TemplateResponse, paginate
from mezzanine.conf import settings
from datetime import date
from django.http import JsonResponse
from Welpe.ofertaTrabajo.utils import OfertasUtils
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q


utils = OfertasUtils()


def clear_filter(request):
    '''
    Esta funcion elimina los filtros aplicados
    :param request: request-post(en un principio) request-gest(por si ponen la url)
    :return: redirect a list_ofertas
    '''
    return redirect(list_ofertas)


def list_ofertas(request, template="/pages/ofertas_list.html"):
    '''
    Esta funcion devuelve una lista de todos las oferta, ordenados por destacados y luego por fecha de inicio
    :param request: request-get
    :param template: events_list
    :return: template(events_list) rellenado con los eventos
    '''
    listado_ofertas = OfertaTrabajo.objects.published()
    filtrar_like = False
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            listado_ofertas = listado_ofertas.filter(Q(title__icontains=content) | Q(descripcion__icontains=content))
        # todo sacar el resto de parametros
        tipo_contrato = request.POST['tipo_contrato']
        if tipo_contrato != '':
            listado_ofertas = listado_ofertas.filter(tipo_contrato=tipo_contrato)
        try:
            like = request.POST['like']
            if like:
                filtrar_like = True
        except:
            pass
    templates = []
    templates.append(u'pages/ofertas_list.html')
    # context = {"lista": lista, "most_viewed_talks":most_viewed_talks, "most_rated_talks":most_rated_talks}
    listado_ofertas = utils.getLikeCommentOfertas(request.user, listado_ofertas, filtrar_like)
    context = {"lista": listado_ofertas}
    templates.append(template)
    context = {"lista": listado_ofertas}
    templates.append(template)
    return TemplateResponse(request, templates, context)


def view_oferta(request, oferta=None, template="pages/oferta.html"):
    '''
    Esta funcion te muestra la oferta seleccionada
    :param request: reques-get
    :param oferta: oferta seleccionada
    :param template: events
    :return: template(events) rellenado con los datos del evento seleccionado
    '''
    oferta = utils.getOferta(oferta)

    today = date.today()
    like = utils.getLikeOferta(oferta, request.user)
    number_of_likes = LikeOferta.objects.filter(oferta=oferta).count()
    comments = CommentsOferta.objects.filter(oferta=oferta)

    context = {"oferta": oferta,
               "today": today,
               "likeOferta": like,
               "comments": comments,
               "number_of_likes": number_of_likes
               }
    templates = []
    templates.append(u'pages/oferta.html')
    templates.append(template)
    return TemplateResponse(request, templates, context)


@login_required
def add_comment(request, oferta):
    """Devuelve la pagina del foro y almacena comentarios nuevos"""
    oferta = utils.getOferta(oferta)
    if request.method == "POST":
        titulo = utils.getfromPost(request, "title")
        comentario=utils.getfromPost(request, "comentario")
        try:
            existe=request.POST['anonimo']
            anonimo = True
        except:
            anonimo=False
        new_comment = CommentsOferta(titulo=titulo, comentario=comentario, oferta=oferta, usuario=request.user, anonimo=anonimo)
        new_comment.save()
    return redirect(oferta)

@login_required
def like_oferta(request, oferta=None):
    '''
    Esta funcion es para saber el numero de usuarios registrados a un evento que van a asistir a una ponencia
    :param request: el request para sacar los datos
    :param oferta: el evento donde se encuentra la ponencia
    :return: retorna un json que cuenta el numero de users preregistrados y los muestra
    '''

    oferta = utils.getOferta(oferta)
    if request.POST:
        guardado = utils.getLikeOferta(oferta, request.user)
        if guardado:
            guardado.delete()

            return JsonResponse({'status': 'unliked',
                                 'number_of_likes': LikeOferta.objects.filter(oferta=oferta).count()})
        else:
            # guargar el preregistro
            new_like = LikeOferta(oferta=oferta, usuario=request.user)

            new_like.save()
            return JsonResponse({'status': 'like',
                                 'number_of_likes': LikeOferta.objects.filter(oferta=oferta).count()})

        return JsonResponse({'status': 'error'})


@login_required
def add_oferta(request):
    '''
    Esta funcion crea o modifica un nuevo evento
    :param request: el request
    :return: retorna a la pagina principal del evento creado o modificado
    '''
    if not request.POST:
        return redirect("home_ofertas")
    # get the father
    parent = Page.objects.get_by_natural_key("ofertas")

    # saco los campos del formulario
    pk = utils.getfromPost(request, 'pk')
    title = utils.getfromPost(request, 'title')

    descripcion = utils.getfromPost(request, 'descripcion')
    como_aplicar = utils.getfromPost(request, 'como_aplicar')
    url = utils.getfromPost(request, 'url')
    cuando = utils.getfromPost(request, 'cuando')
    donde = utils.getfromPost(request, 'donde')
    salario = utils.getfromPost(request, 'salario')
    tipo_contrato = request.POST['tipo_contrato']
    if tipo_contrato == 'Prácticas':
        tipo_contrato = 0
    elif tipo_contrato == 'Indefinido':
        tipo_contrato = 1
    elif tipo_contrato == 'Otros':
        tipo_contrato = 2
    delete_file = utils.getfromPost(request, "delete_file")
    attached_file = utils.getfilefromPost(request, 'archivo')
    if attached_file == "/static/media/":
        attached_file = ""
    try:
        oferta = utils.getOfertaByPK(pk)
    except ObjectDoesNotExist, e:
        oferta = None
    unlinkarchivo = False
    if delete_file:
        unlinkarchivo = True
        if oferta:
            cola, fichero = os.path.split(oferta.attached_file.path)
            oferta.attached_file.delete()

    if oferta and attached_file:
        if oferta.attached_file:
            cola, fichero = os.path.split(oferta.attached_file.path)
            oferta.attached_file.delete()

    if unlinkarchivo and not attached_file:
        attached_file = ""
    # TODO: cambiar espacios por guiones
    if oferta:
        oferta.title = title.decode('utf-8')
        oferta.descripcion = descripcion
        oferta.como_aplicar = como_aplicar
        oferta.url = url
        oferta.cuando = cuando
        oferta.donde = donde
        oferta.salario = salario
        oferta.owner = request.user
        oferta.tipo_contrato = tipo_contrato
        oferta.attached_file = attached_file
        oferta.slug = "ofertas/" + unicode(title, "utf-8")  # si cambia el titulo quiero que cambie el slug
    else:
        oferta = OfertaTrabajo(
            title=title,
            descripcion=descripcion,
            como_aplicar=como_aplicar,
            url=url,
            cuando=cuando,
            donde=donde,
            salario=salario,
            owner=request.user,
            tipo_contrato=tipo_contrato,
            parent=parent,
            slug="ofertas/" + unicode(title, "utf-8"),
            attached_file=""
        )
        # guardamos antes para que el evento tenga id
        oferta.save()
        oferta.attached_file = attached_file
    oferta.save()

    return redirect(oferta)


@login_required
def delete_oferta(request):
    '''
    Delete the event received as parameter via Form
    :param request: The request
    :return: redirect to /events
    '''
    if request.POST:
        pk = utils.getfromPost(request, "pk")
        if pk:
            oferta = utils.getOfertaByPK(pk=pk)
        else:
            raise Exception("Cant delete this event")
        oferta.delete()
    return redirect("home_ofertas")

