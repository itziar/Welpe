# coding=utf-8

from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from Welpe.foro.utils import ForoUtils
from django.shortcuts import redirect
from mezzanine.utils.views import TemplateResponse, paginate
from .models import Foro

utils = ForoUtils()


def list_foro(request, template="pages/list_foro.html"):
    templates = []
    templates.append(u'pages/list_foro.html')
    templates.append(template)
    comments = Foro.objects.all()
    context = {"comments": comments}
    return TemplateResponse(request, templates, context)


@login_required
def add_comment(request):
    """Devuelve la pagina del foro y almacena comentarios nuevos"""
    if request.method == "POST":
        titulo = utils.getfromPost(request, "title")
        comentario = utils.getfromPost(request, "comentario")
        new_comment = Foro(titulo=titulo, comentario=comentario, usuario=request.user)
        new_comment.save()
    return redirect(list_foro)
