from django.shortcuts import render
import os

def handler404(request):
    return render(request,"pages/error404.html", status=404)


def handler403(request):
    return render(request,"pages/error403.html", status=403)


def handler500(request):
    return render(request,"pages/error500.html", status=500)


class UtilsForAll:
    def getfromPost(self, request, campo=None):
        """Given a field return its value if exists. Return an empty string otherwise."""
        if campo is None:
            return ''
        if campo in request.POST:
            return request.POST[campo].strip().encode('utf8')
        return ''

    def getfilefromPost(self, request, campo=None):
        """Given a field return its value if exists. Return an empty string otherwise."""
        if campo is None:
            return ''
        if campo in request.FILES:
            return request.FILES[campo]
        return ''
