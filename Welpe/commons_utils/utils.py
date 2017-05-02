from django.core.exceptions import ObjectDoesNotExist

from django.utils.crypto import get_random_string

from django.contrib.sites.models import Site
from Welpe.profile.models import Comments

class AllUtils:
    def getfromPost(self, request, campo=None, default=None):
        if campo is None or campo not in request.POST:
            if default:
                return default
            return ''
        if request.POST:
            return request.POST[campo].strip()
        return ''


    def getfrom_get(self, request, campo=None, default=None):
        if campo is None or campo not in request.GET:
            if default:
                return default
            return ''
        if request.GET:
            return request.GET[campo].strip()
        return ''


    def getfrom_session(self, request, campo=None, default=None):
        if campo is None or campo not in request.session:
            if default:
                return default
            return ''
        if request.GET:
            return request.session[campo].strip()
        return ''


    def getExcelHeader_for_feedback(self):
        """
        :param event: The event we export to excel
        :return: The row that will be header of our table
        """
        columns = []
        columns.append((u"id", 2000))
        columns.append((u"title", 4000))
        columns.append((u"description", 5000))
        columns.append((u"type", 10000))
        columns.append((u"project", 4000))
        columns.append((u"anonymous", 4000))
        columns.append((u"private", 6000))
        columns.append((u"user", 4000))
        columns.append((u"email", 4000))
        columns.append((u"created", 4000))
        columns.append((u"status", 4000))

        return columns


    def getExcelContent_for_feedback(self, feedback):
        """
        :param event: The event we want to export participants or waiting list
        :param participante: The registered user or waiting list user
        :return: the row we need to add in Excel
        """
        columns = []
        columns.append(str(feedback.id).decode("utf-8"))
        columns.append(feedback.title)
        columns.append(feedback.description)
        columns.append(feedback.type.title)
        columns.append(feedback.project.title)
        columns.append(feedback.anonymous)
        columns.append(feedback.private)
        if feedback.anonymous:
            columns.append("Anonymous")
            columns.append("")
        else:
            columns.append(feedback.user.first_name)
            columns.append(feedback.user.email)
        columns.append(feedback.created.strftime("%B %d, %Y"))
        columns.append(feedback.status.title)

        return columns


    def add_comment(self, request):
        page = request.page
        if request.method == "POST":
            titulo = self.getfromPost(request, "title")
            comentario = self.getfromPost(request, "comentario")
            try:
                existe = request.POST['anonimo']
                anonimo = True
            except:
                anonimo = False
            new_comment = Comments(titulo=titulo, comentario=comentario, page=page, usuario=request.user, anonimo=anonimo)
            new_comment.save()
        return page
