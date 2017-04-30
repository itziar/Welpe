# coding=utf-8
from __future__ import unicode_literals

import os

from django.core.exceptions import ObjectDoesNotExist

from .models import Profile, Message

from Welpe.profile.utils import ProfileUtils
from Welpe.manageUser.views import User
from mezzanine.utils.views import TemplateResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

utils = ProfileUtils()


def view_profile(request, user, template='pages/profile.html'):
    usuario = User.objects.get(pk=user)
    try:
        profile = utils.getProfileByUser(usuario)
    except ObjectDoesNotExist, e:
        profile = None
    if request.POST:
        # sacar los datos del formulario
        dni = utils.getfromPost(request, "dni")
        desc = utils.getfromPost(request, "descripcion")
        url = utils.getfromPost(request, "url")
        telefono = utils.getfromPost(request, "telefono")
        location = utils.getfromPost(request, "location")
        titulacion = utils.getfromPost(request, "titulacion")
        curso = utils.getfromPost(request, "curso")
        formacion = utils.getfromPost(request, "formacion")
        puesto = utils.getfromPost(request, "puesto")
        departamento = utils.getfromPost(request, "departamento")
        investigacion = utils.getfromPost(request, "investigacion")
        show_email = utils.getfromPost(request, "show_email")
        if show_email:
            show_email = True
        else:
            show_email = False
        # save formulario
        if not usuario:
            usuario = request.user
        delete_file = utils.getfromPost(request, "delete_file")
        image = utils.getfilefromPost(request, 'image')
        if image == "/static/media/":
            image = ""

        unlinkarchivo = False
        if delete_file:
            unlinkarchivo = True
            if profile:
                cola, fichero = os.path.split(profile.photo.path)
                profile.attached_file.delete()
        if profile and image:
            if profile.photo:
                cola, fichero = os.path.split(profile.photo.path)
                profile.photo.delete()
        if unlinkarchivo and not image:
            image = ""
        if profile:
            profile.usuario = usuario
            profile.dni = dni
            profile.bio = desc
            profile.pagina_web = url
            profile.telefono = telefono
            profile.location = location
            profile.show_email = show_email
            profile.photo = image
            profile.grado = titulacion
            profile.curso = curso
            profile.formacion = formacion
            profile.puesto = puesto
            profile.departamento = departamento
            profile.investigacion = investigacion

        else:
            profile = Profile(
                usuario=usuario,
                dni=dni,
                bio=desc,
                pagina_web=url,
                telefono=telefono,
                location=location,
                show_email=show_email,
                photo=image,
                grado=titulacion,
                curso=curso,
                formacion=formacion,
                puesto=puesto,
                departamento=departamento,
                investigacion=investigacion
            )
        profile.save()
    try:
        grupo = usuario.groups.get()
    except:
        grupo = None
    # sacar favoritos
    likes = utils.getLikes(usuario)
    actividades = utils.getActividades(usuario)
    mensajes = utils.getMensajes(usuario)
    context = {"profile": profile, "user": usuario, "user_pedido": user, "is_profile": True, 'grupo': grupo,
               'likes': likes, 'actividades': actividades, 'mensajes': mensajes}
    templates = [template]
    return TemplateResponse(request, templates, context)


def send_message(request, user):
    # saco los datos del formulario
    if request.POST:
        subject = utils.getfromPost(request, "subject")
        body = utils.getfromPost(request, "body")
        destinatario = User.objects.get(pk=user)
        remitente = request.user

        mensaje = Message(
            destinatario=destinatario,
            remitente=remitente,
            subject=subject,
            body=body
        )
        mensaje.save()
        url = "/profile/" + str(user)
        return HttpResponseRedirect(url)
