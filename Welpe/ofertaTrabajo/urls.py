#from django.conf.urls import patterns, url
from django.conf.urls import *

import views


urlpatterns = [
    url(r'^/add/$', views.add_oferta),
    url(r'^/delete_oferta$', views.delete_oferta),
    url(r'^/(?P<oferta>.*)/$', views.view_oferta),
    url(r'^/(?P<oferta>.*)/like$', views.like_oferta),
    url(r'^/(?P<url>.*)/comentario$', views.add_comment),
    url(r'^/clear$', views.clear_filter),
    url("^/$", views.list_ofertas, name="home_ofertas"),
]

