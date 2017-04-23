# coding=utf-8
from __future__ import unicode_literals
from utils import ActividadesUtils
from django.core.exceptions import ObjectDoesNotExist
from .models import UsuariosRegistradosActividades, UsuariosListaEsperaActividades

utils = ActividadesUtils()


class UtilsRegistros:
    def getListaEspera(self, actividad, user):
        lista_espera = None
        if actividad.lista_espera:
            try:
                if actividad.has_permissions(user):
                    lista_espera = UsuariosListaEsperaActividades.objects.all().filter(actividad=actividad.id)
                else:
                    lista_espera = UsuariosListaEsperaActividades.objects.all().filter(actividad=actividad.id,
                                                                                       usuario=user)
            except ObjectDoesNotExist:
                pass
        return lista_espera

    def getListaEsperaTodos(self, actividad):
        lista_espera = None
        try:
            lista_espera = UsuariosListaEsperaActividades.objects.all().filter(actividad=actividad.id).order_by(
                'fecha_registro')
        except ObjectDoesNotExist:
            pass
        return lista_espera

    def getNumListaEsperaTodos(self, actividad):
        num_Espera = 0
        try:
            num_Espera = UsuariosListaEsperaActividades.objects.filter(actividad=actividad.id).count()
        except ObjectDoesNotExist:
            pass
        return num_Espera

    def getNumTodosParticipantes(self, actividad):
        num_participantes = 0
        try:
            num_participantes = UsuariosRegistradosActividades.objects.filter(actividad=actividad.id).count()
        except ObjectDoesNotExist:
            pass
        return num_participantes

    def getListaParticipantes(self, actividad, user):
        """
        Esta funcion busca los usuarios  registrados a un evento en funcion de los permisos que tenga el usuario
        :param actividad: el evento
        :param user: el usuario
        :return: devuelve o bien todos los participantes o solo el mismo o none
        """
        lista_participantes = None
        try:
            if actividad.has_permissions(user):
                lista_participantes = UsuariosRegistradosActividades.objects.all().filter(actividad=actividad.id)
            else:
                lista_participantes = UsuariosRegistradosActividades.objects.all().filter(actividad=actividad.id,
                                                                                          usuario=user)
        except ObjectDoesNotExist:
            pass
        return lista_participantes

    def getListaTodosParticipantes(self, actividad):
        lista_participantes = None
        try:
            lista_participantes = UsuariosRegistradosActividades.objects.all().filter(actividad=actividad.id)
        except ObjectDoesNotExist:
            pass
        return lista_participantes

    def getDatosInRegistroOrInEspera(self, actividad, user):
        """
        Esta funcion devuelve el usuario registrado a un evento o el usuario en lista de espera para un evento
        :param actividad: evento sobre el que se quiere hacer la busqueda
        :param user: usuario que se espera encontrar registrado o en la lista de espera
        :return: retorna o bien el objeto encontrado (en registro o en lista de espera) o none
        """
        try:
            return UsuariosRegistradosActividades.objects.get(actividad=actividad, usuario=user)
        except ObjectDoesNotExist:
            pass
        try:
            return UsuariosListaEsperaActividades.objects.get(actividad=actividad, usuario=user)
        except ObjectDoesNotExist:
            pass
        return None

    def get_datos_solo_en_registro(self, actividad, user):
        """
        Esta funcion busca si un usuario esta registrado en un evento
        :param actividad: el evento
        :param user: el usuario
        :return: retorna el objeto encontrado o none
        """
        try:
            return UsuariosRegistradosActividades.objects.get(actividad=actividad, usuario=user)
        except ObjectDoesNotExist:
            return None

    def get_datos_solo_en_espera(self, acttividad, user):
        """
        Esta funcion se encarga de buscar un usuario concreto en la lista de espera de un evento en concreto
        :param acttividad: evento sobre el que se quiere hacer la busqueda
        :param user: usuario que se quiere encontrar en la lista de espera
        :return: retorna o bien el objeto encontrado o none dependiendo si ha encontrado al usuario o no
        """
        try:
            return UsuariosListaEsperaActividades.objects.get(actividad=acttividad, usuario=user)
        except ObjectDoesNotExist:
            return None

    def registrate_user_to_actividad(self, request, user, actividad):
        """
        Esta funcion es la encargada de guardar en la bbdd los datos del registro
        :param request: usuario que hace la peticion de registro
        :param user: usuario que hace la peticion de registro
        :param actividad: evento al que el usuario (user) se quiere registrar
        :param user_information: datos del usuario (user) pasados por el formulario
        :return: retorna o bien el objeto encontrado o none dependiendo si ha encontrado al usuario o no
        """
        usuario_registrado = self.getDatosInRegistroOrInEspera(actividad, user)
        title = "Registered to event " + actividad.title
        if usuario_registrado:
            usuario_registrado.save()
        else:
            current_registered = UsuariosRegistradosActividades.objects.filter(actividad=actividad.id).count()
            # miramos si hay limite de participantes o hemos llegado al limite de participantes
            if (not actividad.limite_participantes) or (current_registered < actividad.limit):
                usuarios_registrados = UsuariosRegistradosActividades(actividad=actividad,
                                                                      usuario=user,
                                                                      )
                usuarios_registrados.save()
            else:  # hemos llegado al limite de participantes
                # si hay lista de espera guardamos al user en la lista de espera sino no hacemos nada
                if actividad.lista_espera:
                    usuarios_registrados = UsuariosListaEsperaActividades(actividad=actividad,
                                                                          usuario=user,
                                                                          )
                    usuarios_registrados.save()


    def contador_lista_espera(self, lista_espera, actividad, user):
        contador = 0
        usuario_registrado = self.get_datos_solo_en_espera(actividad, user)
        if usuario_registrado:  # aunque deberia de existir siempre
            fecha_a_filtrar = usuario_registrado.fecha_registro
            contador = lista_espera.filter(fecha_registro__lt=fecha_a_filtrar).count()
        return contador
