# Create your views here.
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.http import JsonResponse
from mezzanine.pages.views import page


def homepage(request):
    request.path = "/"
    return page(request, slug="home")


def check_status(request):
    """
    :return:a json string { "status" : ok} if there is connection to database, error otherwise.
    """
    try:
        number_of_users = User.objects.all().count()
        return JsonResponse({'status':'ok'})
    except DatabaseError as e:
        return JsonResponse({'status':'error', 'info' : e.message})

