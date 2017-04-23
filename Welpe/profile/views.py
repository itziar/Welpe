# coding=utf-8
from __future__ import unicode_literals

import os

from django.core.exceptions import ObjectDoesNotExist

from .models import Profile

from django.shortcuts import render, redirect
# Create your views here.
# Import models
from .models import Message

from Welpe.profile.utils import ProfileUtils
from mezzanine.accounts.views import User
from mezzanine.utils.views import TemplateResponse
from django.contrib.auth.models import User, Group

from mezzanine.accounts.forms import ProfileForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from mezzanine.utils.urls import login_redirect
from django.utils.translation import ugettext_lazy as _

utils = ProfileUtils()


def CreateUser(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # guardamos el form con lo que creamos el usuario
            form.save()
            # sacamos el email
            email = form.clean_email()
            # autenticamos al usuario
            usuario = request.POST['username']
            clave = request.POST['password1']
            acceso = authenticate(username=usuario, password=clave)
            sitio = email.split("@")[1]
            if sitio == "urjc.es":
                try:
                    g = Group.objects.get(name='profesores')
                except:
                    g = Group.objects.create(name="profesores")
                g.user_set.add(acceso)
            else:
                try:
                    g = Group.objects.get(name='alumnos')
                except:
                    g = Group.objects.create(name="alumnos")
                g.user_set.add(acceso)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    # saco el id para redirigir al profile
                    # es una precaucion. nunca deberia entrar en el except
                    try:
                        id = User.objects.get(username=usuario).id
                        url = '/profile/' + str(id)
                    except:
                        url = '/'
                    return HttpResponseRedirect(url)
            return HttpResponseRedirect("/")
    else:
        form = ProfileForm()
    context = {'form': form}
    return render(request, 'pages/create_user.html', context)


def Autenticar(request, template="pages/login.html", form_class=LoginForm):
    form = form_class(request.POST or None)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return login_redirect(request)
    context = {"form": form, "title": _("Login")}
    return TemplateResponse(request, template, context)


def CerrarSesion(request):
    """
        Log the user out.
        """
    logout(request)
    return HttpResponseRedirect("/")


def view_profile(request, user, template='pages/profile.html'):
    """
    Esta funcion te muestra la oferta seleccionada
    :param request: reques-get
    :param user: usuario
    :param template: events
    :return: template(events) rellenado con los datos del evento seleccionado
    """
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
    mensajes=utils.getMensajes(usuario)
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
        url="/profile/"+str(user)
        return HttpResponseRedirect(url)
