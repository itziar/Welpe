#from django.conf.urls import patterns, url
from django.conf.urls import *

import views


urlpatterns = [
    url("^/$", views.list_foro, name="home_foro"),
    url(r'^/add_comment/$', views.add_comment),
]

