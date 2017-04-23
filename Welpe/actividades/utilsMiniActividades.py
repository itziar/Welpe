from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from .models import MiniActividad, AsistentesMiniActividad, OrganizadorMiniActividad


class UtilsMiniActividades:
    # solo se hace para mostrar la actividad
    def getMiniActividades(self, actividad, usuario):
        listado_miniactividades = MiniActividad.objects.all().filter(actividad=actividad).order_by('fecha', 'hora', 'id')
        listado_miniactividades_asistentes = []
        if usuario.is_authenticated:
            for elemento in listado_miniactividades:
                miniactividades = {}
                miniactividades["miniactividad"] = elemento
                miniactividades["asistentes"] = AsistentesMiniActividad.objects.filter(miniactividad=elemento).count()
                try:
                    AsistentesMiniActividad.objects.get(miniactividad=elemento, usuario=usuario)
                    miniactividades["preregistrado"] = True
                except ObjectDoesNotExist, e:
                    miniactividades["preregistrado"] = False
                    miniactividades["autores"] = AsistentesMiniActividad.objects.all().filter(miniactividad=elemento)
                listado_miniactividades_asistentes.append(miniactividades)
        else:
            for elemento in listado_miniactividades:
                miniactividades = {}
                miniactividades["miniactividad"] = elemento
                miniactividades["asistentes"] = AsistentesMiniActividad.objects.filter(miniactividad=elemento).count()
                miniactividades["preregistrado"] = False
                miniactividades["autores"] = AsistentesMiniActividad.objects.all().filter(miniactividad=elemento)
                listado_miniactividades_asistentes.append(miniactividades)
        return listado_miniactividades_asistentes

    def getMiniActividad(self, actividad, pk):
        listado_ponencias = None
        try:
            listado_ponencias = MiniActividad.objects.get(actividad=actividad, pk=pk)
        except ObjectDoesNotExist, e:
            pass
        return listado_ponencias

    def getMiniActividadOrganizador(self, actividad, miniactividad_pk, pk):
        '''
        Get a speech author
        :param event: The event
        :param speech: The event speech
        :param pk: The primary key of the author
        :return: The SpeechAuthor object
        '''
        listado_authors = None
        try:
            miniactividad = self.getMiniActividad(actividad, miniactividad_pk)
            listado_authors = OrganizadorMiniActividad.objects.get(miniactividad=miniactividad, pk=pk)
        except ObjectDoesNotExist, e:
            pass
        return listado_authors
