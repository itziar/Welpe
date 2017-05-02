# coding=utf-8
from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from mezzanine.utils.views import TemplateResponse

from Welpe.manageUser.views import User
from Welpe.profile.utils import ProfileUtils
from .models import Profile, Message, ProfileProfesor, ProfileAlumno

utils = ProfileUtils()


def view_profile(request, user, template='pages/profile.html'):
    user = User.objects.get(pk=user)
    try:
        profile = utils.getProfileByUser(user)
    except ObjectDoesNotExist, e:
        profile = None
    try:
        grupo = user.groups.get()
    except:
        grupo = None
    if request.POST:
        # sacar los datos del formulario
        dni = utils.getfromPost(request, "dni")
        desc = utils.getfromPost(request, "descripcion")
        url = utils.getfromPost(request, "url")
        telefono = utils.getfromPost(request, "telefono")
        location = utils.getfromPost(request, "location")
        show_email = utils.getfromPost(request, "show_email")
        if show_email:
            show_email = True
        else:
            show_email = False
        # save formulario
        if not user:
            user = request.user
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
            profile.usuario = user
            profile.dni = dni
            profile.bio = desc
            profile.pagina_web = url
            profile.telefono = telefono
            profile.location = location
            profile.show_email = show_email
            profile.photo = image
        else:
            profile = Profile(
                usuario=user,
                dni=dni,
                bio=desc,
                pagina_web=url,
                telefono=telefono,
                location=location,
                show_email=show_email,
                photo=image,
            )
        profile.save()
        if grupo.name == "profesores":
            formacion = utils.getfromPost(request, "formacion")
            puesto = utils.getfromPost(request, "puesto")
            departamento = utils.getfromPost(request, "departamento")
            investigacion = utils.getfromPost(request, "investigacion")
            try:
                profesor = utils.getProfileProfesorByUser(user)
            except ObjectDoesNotExist, e:
                profesor = None
            if profesor:
                profesor.usuario = user
                profesor.formacion = formacion
                profesor.puesto = puesto
                profesor.departamento = departamento
                profesor.investigacion = investigacion
            else:
                profesor = ProfileProfesor(
                    usuario = user,
                    formacion=formacion,
                    puesto=puesto,
                    departamento=departamento,
                    investigacion=investigacion
                )
            profesor.save()
        if grupo.name == "alumnos":
            titulacion = utils.getfromPost(request, "titulacion")
            curso = utils.getfromPost(request, "curso")
            try:
                alumno = utils.getProfileAlumnoByUser(user)
            except ObjectDoesNotExist, e:
                alumno = None
            if alumno:
                alumno.usuario = user
                alumno.grado = titulacion
                alumno.curso = curso
            else:
                alumno = ProfileAlumno(
                    usuario = user,
                    grado=titulacion,
                    curso=curso,
                )
            alumno.save()
            # sacar favoritos
    perfil_profesor=None
    if grupo.name == "profesores":
        try:
            perfil_profesor = utils.getProfileProfesorByUser(user)
        except ObjectDoesNotExist, e:
            perfil_profesor = None
    perfil_alumno = None
    if grupo.name == "alumnos":
        try:
            perfil_alumno = utils.getProfileAlumnoByUser(user)
        except ObjectDoesNotExist, e:
            perfil_alumno = None
    likes = utils.getLikes(user)
    actividades = utils.getActividades(user)
    mensajes = utils.getMensajes(user)
    context = {"profile": profile, "user": user, "is_profile": True, 'grupo': grupo,
               'likes': likes, 'actividades': actividades, 'mensajes': mensajes, "profile_profesor": perfil_profesor, "profile_alumno": perfil_alumno}
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
