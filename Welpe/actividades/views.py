# coding=utf-8
from __future__ import unicode_literals

import os
from datetime import date

import xlwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import redirect
from mezzanine.conf import settings
from mezzanine.pages.models import Page
from mezzanine.utils.views import TemplateResponse

from Welpe.actividades.utils import ActividadesUtils
from Welpe.actividades.utilsMiniActividades import UtilsMiniActividades
from Welpe.actividades.utilsRegistros import UtilsRegistros
from Welpe.commons_utils.utils import AllUtils
from Welpe.manageUser.views import User
from Welpe.profile.models import Comments
from Welpe.profile.models import LikeActividad
from .models import Actividades, MiniActividad, UsuariosRegistradosActividades, \
    OrganizadorMiniActividad

utils = ActividadesUtils()
utilsRegistros = UtilsRegistros()
utilsMiniActividades = UtilsMiniActividades()
utilsAll = AllUtils()


def clear_filter(request):
    '''
    Esta funcion elimina los filtros aplicados
    :param request: request-post(en un principio) request-gest(por si ponen la url)
    :return: redirect a list_ofertas
    '''
    return redirect(list_actividades)


def list_actividades(request, template="pages/actividades_list.html"):
    """
    Esta funcion devuelve una lista de todos los actividades, ordenados por fecha de inicio
    :param request: request-get
    :param template: seminarios_list
    :return: template(seminarios_list) rellenado con los actividades
    """
    lista = Actividades.objects.published().order_by("-destacado", "-start_date")
    filtrar_like = False
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            lista = lista.filter(Q(title__icontains=content) | Q(descripcion__icontains=content))
        # todo sacar el resto de parametros
        try:
            like = request.POST['like']
            if like:
                filtrar_like = True
        except:
            pass
    templates = []
    # lista = paginate(lista, request.GET.get("page", 1),
    #                 settings.BLOG_POST_PER_PAGE,
    #                 settings.MAX_PAGING_LINKS)
    templates.append(u'pages/actividades_list.html')
    lista = utils.getLikeCommentActividades(request.user, lista, filtrar_like)

    # context = {"lista": lista, "most_viewed_talks":most_viewed_talks, "most_rated_talks":most_rated_talks}
    context = {"lista": lista}
    templates.append(template)
    return TemplateResponse(request, templates, context)


def view_actividad(request, actividad=None, template="pages/actividad.html"):
    """
     Esta funcion te muestra el seminario seleccionado
     :param request: reques-get
     :param actividad: seminario seleccionado
     :param template: seminario
     :return: template(seminario) rellenado con los datos del seminario seleccionado
     """
    actividad = utils.getActividad(actividad)
    if request.user:
        like = utils.getLikeActividad(actividad, request.user)
    else:
        like = False
    number_of_likes = LikeActividad.objects.filter(actividad=actividad).count()
    lista_participantes = utilsRegistros.getListaTodosParticipantes(actividad)
    lista_espera = utilsRegistros.getListaEsperaTodos(actividad)
    is_registered = False
    if lista_participantes:
        for usuarios_registrados in lista_participantes:
            if request.user == usuarios_registrados.usuario:
                is_registered = True
    is_registered_espera = False
    if lista_espera:
        for usuarios_registrados in lista_espera:
            if request.user == usuarios_registrados.usuario:
                is_registered_espera = True
    today = date.today()
    if actividad.permitir_inscriptions:
        inicio_registro = utils.comparar_fechas_inicio(today, actividad.fecha_inscripcion_inicio)
        final_registro = utils.comparar_fechas_final(today, actividad.fecha_inscripcion_final)
    else:
        inicio_registro = False
        final_registro = False
    # metemos el usuario para que nos diga si esta o no registrado en la ponencia
    listado_miniactividades = utilsMiniActividades.getMiniActividades(actividad, request.user)

    comments = Comments.objects.filter(page=request.page)
    context = {"actividad": actividad,
               "inicio_registro": inicio_registro,
               "final_registro": final_registro,
               "today": today,
               "is_registered": is_registered,
               "is_registered_espera": is_registered_espera,
               "lista_espera": lista_espera,
               "lista_participantes": lista_participantes,
               "listado_miniactividades": listado_miniactividades,
               "comments": comments,
               'likeAct': like,
               'number_of_likes': number_of_likes,
               }
    templates = [template]
    return TemplateResponse(request, templates, context)


@login_required
def add_comment(request, url):
    """Devuelve la pagina del foro y almacena comentarios nuevos"""
    page = utilsAll.add_comment(request)
    return redirect(page)


@login_required
def like_actividad(request, actividad=None):
    '''
    Esta funcion es para saber el numero de usuarios registrados a un evento que van a asistir a una ponencia
    :param request: el request para sacar los datos
    :param oferta: el evento donde se encuentra la ponencia
    :return: retorna un json que cuenta el numero de users preregistrados y los muestra
    '''
    actividad = utils.getActividad(actividad)
    if request.POST:
        guardado = utils.getLikeActividad(actividad, request.user)
        if guardado:
            guardado.delete()
            return JsonResponse({'status': 'unliked',
                                 'number_of_likes': LikeActividad.objects.filter(actividad=actividad).count()})
        else:
            new_like = LikeActividad(actividad=actividad, usuario=request.user)
            new_like.save()
            return JsonResponse({'status': 'like',
                                 'number_of_likes': LikeActividad.objects.filter(actividad=actividad).count()})
        return JsonResponse({'status': 'error'})


def add_actividad(request):
    """
    Esta funcion crea o modifica un nuevo evento
    :param request: el request
    :return: retorna a la pagina principal del evento creado o modificado
    """
    if not request.POST:
        return redirect("home_actividades")
    # get the father
    parent = Page.objects.get_by_natural_key("actividades")
    # saco los campos del formulario
    pk = utils.getfromPost(request, 'pk')
    start_date = utils.getfromPost(request, 'start_date')
    finish_date = utils.getfromPost(request, 'finish_date')
    url = utils.getfromPost(request, 'url')
    adminlist = utils.getfromPost(request, 'adminlist')
    title = utils.getfromPost(request, 'title')
    descripcion_actividad = utils.getfromPost(request, 'descripcion')
    permitir_inscriptions = utils.getfromPost(request, 'permitir_inscriptions')
    fecha_inscripcion_inicio = utils.getfromPost(request, 'fecha_inscripcion_inicio')
    fecha_inscripcion_final = utils.getfromPost(request, 'fecha_inscripcion_final')
    limite_participantes = utils.getfromPost(request, 'limite_participantes')
    limit = utils.getfromPost(request, 'limit')
    creditos = utils.getfromPost(request, 'creditos')
    creditos_etsi = utils.getfromPost(request, 'creditos_etsi')
    lugar = utils.getfromPost(request, 'lugar')
    lista_espera = utils.getfromPost(request, 'lista_espera')
    enviar_notificaciones = utils.getfromPost(request, 'enviar_notificaciones')
    email_organizador = utils.getfromPost(request, 'email_organizador')
    delete_file = utils.getfromPost(request, "delete_file")
    attached_file = utils.getfilefromPost(request, 'archivo')
    incluir_miniactividades = utils.getfromPost(request, 'incluir_miniactividades')
    destacado = utils.getfilefromPost(request, 'destacado')
    in_menus = False
    if incluir_miniactividades:
        incluir_miniactividades = True
    else:
        incluir_miniactividades = False
    if destacado:
        destacado = True
    else:
        destacado = False
    if permitir_inscriptions:
        permitir_inscriptions = True
    else:
        permitir_inscriptions = False
    if limite_participantes:
        limite_participantes = True
    else:
        limite_participantes = False
    if creditos:
        creditos = True
    else:
        creditos = False
    if enviar_notificaciones:
        enviar_notificaciones = True
    else:
        enviar_notificaciones = False
    if lista_espera:
        lista_espera = True
    else:
        lista_espera = False

    if attached_file == "/static/media/":
        attached_file = ""
    if not limit:
        limit = None
    if not creditos_etsi:
        creditos_etsi = None
    if not fecha_inscripcion_inicio:
        fecha_inscripcion_inicio = None
    if not fecha_inscripcion_final:
        fecha_inscripcion_final = None
    try:
        actividad = utils.getActividadByPK(pk)
    except ObjectDoesNotExist, e:
        actividad = None
    unlinkarchivo = False
    if delete_file:
        unlinkarchivo = True
        if actividad:
            cola, fichero = os.path.split(actividad.attached_file.path)
            actividad.attached_file.delete()

    if actividad and attached_file:
        if actividad.attached_file:
            cola, fichero = os.path.split(actividad.attached_file.path)
            actividad.attached_file.delete()

    if unlinkarchivo and not attached_file:
        attached_file = ""
    if actividad:
        actividad.incluir_miniactividades = incluir_miniactividades
        actividad.destacado = destacado
        actividad.start_date = start_date
        actividad.finish_date = finish_date
        actividad.url = url
        actividad.adminlist = adminlist
        actividad.title = title.decode('utf-8')  # \mezzanine\pages\models.py in save  self.titles = " / ".join(titles)
        actividad.descripcion = descripcion_actividad.decode('utf-8')
        actividad.permitir_inscriptions = permitir_inscriptions
        actividad.fecha_inscripcion_inicio = fecha_inscripcion_inicio
        actividad.fecha_inscripcion_final = fecha_inscripcion_final
        actividad.limite_participantes = limite_participantes
        actividad.limit = limit
        actividad.creditos = creditos
        actividad.creditos_etsi = creditos_etsi
        actividad.lugar = unicode(lugar, "utf-8")
        actividad.lista_espera = lista_espera
        actividad.enviar_notificaciones = enviar_notificaciones
        actividad.email_organizador = email_organizador
        if attached_file or unlinkarchivo:
            actividad.attached_file = attached_file
        actividad.in_menus = in_menus
    else:
        actividad = Actividades(
            start_date=start_date,
            finish_date=finish_date,
            destacado=destacado,
            incluir_miniactividades=incluir_miniactividades,
            url=url,
            adminlist=adminlist,
            title=title.decode('utf-8'),  # \mezzanine\pages\models.py in save  self.titles = " / ".join(titles)
            descripcion=descripcion_actividad.decode('utf-8'),
            permitir_inscriptions=permitir_inscriptions,
            fecha_inscripcion_inicio=fecha_inscripcion_inicio,
            fecha_inscripcion_final=fecha_inscripcion_final,
            limite_participantes=limite_participantes,
            limit=limit,
            creditos_rac=creditos,
            n_rac=creditos_etsi,
            lugar=unicode(lugar, "utf-8"),
            parent=parent,
            lista_espera=lista_espera,
            enviar_notificaciones=enviar_notificaciones,
            owner=request.user,
            email_organizador=email_organizador,
            attached_file="",
            in_menus=in_menus,
        )
        # guardamos antes para que el evento tenga id
        actividad.save()
        actividad.attached_file = attached_file
    actividad.save()
    return redirect(actividad)


def delete_actividad(request):
    """
    Delete the event received as parameter via Form
    :param request: The request
    :return: redirect to /events
    """
    if request.POST:
        pk = utils.getfromPost(request, "pk")
        if pk:
            actividad = utils.getActividadByPK(pk=pk)
        else:
            raise Exception("Cant delete this event")
        if not actividad.has_permissions(request.user):
            return HttpResponseForbidden()
        actividad.delete()
    return redirect("home_actividades")


def registrate(request, actividad=None):
    """
    Esta funcion registra o modifica el registro de un usuario a un evento
    :param request: request-post
    :param actividad: evento al que se quiere registrar
    :return: retorna a la pagina principal del evento
    """
    actividad = utils.getActividad(actividad)

    # formulario de registro del evento sacamos los datos del formulario
    if request.POST:
        today = date.today()
        id_usuario = utils.getfromPost(request, "id_usuario")
        if not utils.has_permission_registration(actividad, request.user):
            return HttpResponseForbidden("Can't add or modify registration from this event")
        if id_usuario:
            user = User.objects.get(id=id_usuario)
        else:
            if today < actividad.fecha_inscripcion_inicio or today > actividad.fecha_inscripcion_final:
                return HttpResponseForbidden("Can't register on this date. Please, check registration dates")
            user = request.user
        utilsRegistros.registrate_user_to_actividad(request=request, user=user, actividad=actividad)
    else:
        templates = ["pages/form_registro.html"]

        participante = utilsRegistros.getDatosInRegistroOrInEspera(actividad, request.user)
        today = date.today()

        context = {"actividad": actividad,
                   "tipo": "registration",
                   "datos": participante,
                   "today": today,
                   }
        return TemplateResponse(request, templates, context)

    return redirect(actividad)


# eliminar un participante de un evento
@login_required
def delete_user_actividad(request, actividad=None):
    """
    Eliminamos el usuario de la bbdd
    :param request: request-post
    :param actividad: evento del cual el usuario se borra
    :return: retorna a la pagina principal del evento
    """
    actividad = utils.getActividad(actividad)
    title = settings.UNSUB_TEXT + actividad.title
    id_usuario = utils.getfromPost(request, "id_usuario")
    if not id_usuario:
        raise Exception("Cant delete empty user")
    user = User.objects.get(id=id_usuario)
    if not actividad.has_permissions(request.user) and not user == request.user:
        return HttpResponseForbidden("Can't cancel registration from other")
    if not utils.has_permission_registration(actividad, request.user):
        return HttpResponseForbidden("Can't delete registration from this event")
    # formulario de registro del evento
    if request.POST:
        # intentamos buscar el usuario en la tabla de participantes registrados
        usuario_registrado = utilsRegistros.get_datos_solo_en_registro(actividad, user)
        if usuario_registrado:
            usuario_registrado.delete()

            if actividad.lista_espera:
                # tengo los usuarios en espera ordenados por fecha de registro
                usuarios_espera = utilsRegistros.getListaEsperaTodos(actividad)
                if usuarios_espera and usuarios_espera.count() > 0:
                    usuario_espera = usuarios_espera[0]
                    usuario_registrado = UsuariosRegistradosActividades(actividad=actividad,
                                                                        usuario=usuario_espera.usuario,
                                                                        )
                    usuario_registrado.save()

                    usuario_espera.delete()
        else:
            usuario_registrado_espera = utilsRegistros.get_datos_solo_en_espera(actividad, user)
            usuario_registrado_espera.delete()

    return redirect(actividad)


@login_required
def download(request, actividad=None):
    """
    This function downloads content in Excel Format

    :param request: This is the request
    :param actividad: The event we are talking about
    :return: a Excel file with the content we are showing
    """
    if not actividad:
        raise Exception("Fatal error. Should not be here")
    actividad = utils.getActividad(actividad)

    if not request.POST:
        return redirect(actividad)

    what = utils.getfromPost(request, "what")

    if what == "registered":
        lista = utilsRegistros.getListaParticipantes(actividad, request.user)
        headers = utils.getExcelHeader_for_register(actividad)

    elif what == "waiting":
        lista = utilsRegistros.getListaEspera(actividad, request.user)
        headers = utils.getExcelHeader_for_register(actividad)

    else:
        raise Exception("Fatal error. Parameters are incorrect")

    if not lista:
        return redirect(actividad)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + what + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("download")

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in xrange(len(headers)):
        ws.write(row_num, col_num, headers[col_num][0], font_style)
        ws.col(col_num).width = headers[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for item in lista:
        row_num += 1
        if what == "registered" or what == "waiting":
            row = utils.getExcelContent_for_register(item)
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def add_miniactividad(request, actividad=None):
    """
    Esta funcion add o modifica una ponencia en un evento dado
    :param request: el request
    :param actividad: el evento
    :return: retorna a la pagina principal del evento
    """
    actividad = utils.getActividad(actividad)
    # mirarmos si tiene permisos sobre el evento
    if not actividad.has_permissions(request.user):
        return HttpResponseForbidden("Can't add or edit miniactividad for this actividad")
    # formulario de regitro de ponencia
    if request.POST:
        # saco los campos del formulario
        pk = utils.getfromPost(request, 'pk')
        titulo = utils.getfromPost(request, 'titulo')
        descripcion = utils.getfromPost(request, 'description')
        place = utils.getfromPost(request, 'place')
        fecha = utils.getfromPost(request, 'fecha')
        hora = utils.getfromPost(request, 'hora')
        miniactividad = None
        if pk:
            miniactividad = utilsMiniActividades.getMiniActividad(actividad, pk=pk)
        delete_image = utils.getfromPost(request, "delete_image")
        unlinkarchivo = False
        if delete_image:
            unlinkarchivo = True
            if miniactividad:
                cola, fichero = os.path.split(miniactividad.archivo.path)
                miniactividad.archivo.delete()
        archivo = utils.getfilefromPost(request, 'archivo')
        if miniactividad and archivo:
            if miniactividad.archivo:
                cola, fichero = os.path.split(miniactividad.archivo.path)
                miniactividad.archivo.delete()

        if unlinkarchivo and not archivo:
            archivo = ""
        # comprobar si se esta modificando
        if miniactividad:
            miniactividad.titulo = titulo
            miniactividad.descripcion = descripcion
            miniactividad.place = place
            miniactividad.fecha = fecha
            miniactividad.hora = hora
            miniactividad.archivo = archivo
        else:
            miniactividad = MiniActividad(actividad=actividad,
                                          titulo=titulo,
                                          place=place,
                                          fecha=fecha,
                                          hora=hora,
                                          descripcion=descripcion,
                                          archivo="", )
            # guardamos antes para que la ponencia tenga id
            miniactividad.save()
            miniactividad.archivo = archivo
        # save
        miniactividad.save()
        return redirect(actividad)


def delete_miniactividad(request, actividad=None):
    """
    Delete a proposal
    :param request: The request
    :param actividad: The event
    :return: homepage of the event
    """
    actividad = utils.getActividad(actividad)
    # miramos si tiene permisos sobre el evento
    if not actividad.has_permissions(request.user):
        return HttpResponseForbidden("Can't delete miniactividad for this actividad")
    # formulario de eliminacion de una ponencia
    if request.POST:
        # saco los campos del formulario
        pk = utils.getfromPost(request, "pk")
        if pk:
            miniactividad = utilsMiniActividades.getMiniActividad(actividad, pk=pk)
        else:
            raise Exception("Cant delete your speech for this event")
        if miniactividad:
            miniactividad.delete()
    return redirect(actividad)


def add_organizador_miniactividad(request, actividad=None):
    """
    Add an author to a speech
    :param request: The request
    :param actividad: The event
    :return: homepage of the event
    """
    actividad = utils.getActividad(actividad)
    # formulario de regitro de ponencia
    if not actividad.has_permissions(request.user):
        return HttpResponseForbidden("Can't add or edit author for this actividad")
    if request.POST:
        # saco los campos del formulario
        pk = utils.getfromPost(request, 'pk')
        miniactividad_pk = utils.getfromPost(request, 'speech_pk')
        name = utils.getfromPost(request, 'name')
        email = utils.getfromPost(request, 'email')
        bio = utils.getfromPost(request, 'bio')
        company = utils.getfromPost(request, 'company')
        photo = utils.getfromPost(request, 'image')
        miniactividad = utilsMiniActividades.getMiniActividad(actividad, miniactividad_pk)
        if pk:
            miniactividad_organizador = utilsMiniActividades.getMiniActividadOrganizador(actividad,
                                                                                         miniactividad_pk=miniactividad_pk,
                                                                                         pk=pk)
            miniactividad_organizador.name = name.decode("utf-8")
            miniactividad_organizador.bio = bio
            miniactividad_organizador.email = email
            miniactividad_organizador.company = company
            miniactividad_organizador.photo = unicode(photo, "utf-8")
        else:
            miniactividad_organizador = OrganizadorMiniActividad(miniactividad=miniactividad,
                                                                 name=name.decode("utf-8"),
                                                                 bio=bio,
                                                                 email=email,
                                                                 company=company,
                                                                 photo=unicode(photo, "utf-8"))
            miniactividad_organizador.save()
        return redirect(actividad)


def delete_organizador_miniactividad(request, actividad=None):
    """
    Delete a speech author
    :param request: The request
    :param actividad: The event
    :return: homepage of the event
    """
    actividad = utils.getActividad(actividad)
    if request.POST:
        # saco los campos del formulario
        pk = utils.getfromPost(request, "pk")
        miniactividad_pk = utils.getfromPost(request, "miniactividad_pk")
        if pk:
            organizador_miniactividad = utilsMiniActividades.getMiniActividadOrganizador(actividad, miniactividad_pk,
                                                                                         pk=pk)
        else:
            raise Exception("Cant delete this Author for this event")
        if organizador_miniactividad:
            organizador_miniactividad.delete()
    return redirect(actividad)
