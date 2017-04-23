from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist

from Welpe.site_utils import UtilsForAll
from .models import Profile, LikeInfo, LikeOferta, LikePropuesta, LikeActividad, Message
from Welpe.actividades.models import Actividades, UsuariosRegistradosActividades, UsuariosListaEsperaActividades

utilsForAll = UtilsForAll()


def get_mail_list(actividad):
    # lista de administradores a quien redirigir el correo de la actividad
    cc = actividad.adminlist.replace(";", " ").replace(",", " ").split()
    cc.append(actividad.owner.email)
    return cc


class ProfileUtils:
    def getfromPost(self, request, campo=None):
        """Given a field return its value if exists. Return an empty string otherwise."""
        return utilsForAll.getfromPost(request, campo)

    def getfilefromPost(self, request, campo=None):
        """Given a field return its file value if exists. Return an empty string otherwise."""
        return utilsForAll.getfilefromPost(request, campo)

    def getProfileByUser(self, user=None):
        if not user:
            raise ObjectDoesNotExist()
        try:
            result = Profile.objects.get(usuario=user)
        except ObjectDoesNotExist, e:
            return None
        return result

    def getLikes(self, user):
        favs_info = LikeInfo.objects.filter(usuario=user)
        favs_oferta = LikeOferta.objects.filter(usuario=user)
        favs_propuesta = LikePropuesta.objects.filter(usuario=user)
        favs_actividad = LikeActividad.objects.filter(usuario=user)
        return {'favs_info': favs_info, 'favs_oferta': favs_oferta, 'favs_propuesta': favs_propuesta,
                'favs_actividad': favs_actividad}

    def getActividades(self, user):
        lista_registros = UsuariosRegistradosActividades.objects.filter(usuario=user)
        Rlista_actividades = []
        for i in lista_registros:
            try:
                actividad = Actividades.objects.get(pk=i.actividad)
                Rlista_actividades.append(actividad)
            except:
                pass
        lista_espera = UsuariosListaEsperaActividades.objects.filter(usuario=user)
        Elista_actividades = []
        for i in lista_espera:
            try:
                actividad = Actividades.objects.get(pk=i.actividad)
                Elista_actividades.append(actividad)
            except:
                pass
        lista = {"Registro": Rlista_actividades, "Espera": Elista_actividades}
        return lista

    def getMensajes(self, user):
        mensajes_recibidos = Message.objects.filter(destinatario=user)
        mensajes_enviados = Message.objects.filter(remitente=user)
        lista = {"recibidos": mensajes_recibidos, "enviados": mensajes_enviados}
        return lista

    def has_perm(self, user):
        try:
            grupo = user.groups.get()
        except:
            grupo = None
        if user.is_superuser or (grupo.name == "profesores"):
            return True
        else:
            return False
