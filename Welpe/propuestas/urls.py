#from django.conf.urls import patterns, url
from django.conf.urls import *

import views


urlpatterns = [
    url(r'^/add/$', views.add_propuesta),
    url(r'^/delete_propuesta$', views.delete_propuesta),
    url(r'^/(?P<propuesta>.*)/$', views.view_propuesta),
    url(r'^/(?P<propuesta>.*)/like$', views.like_propuesta),
    url(r'^/(?P<url>.*)/comentario$', views.add_comment),
    url(r'^/clear$', views.clear_filter),
    url("^/$", views.list_propuesta, name="home_propuesta"),
]

