#from django.conf.urls import patterns, url
from django.conf.urls import *

import views


urlpatterns = [
    url(r'^/add/$', views.add_info),
    url(r'^/delete$', views.delete_info),
    url(r'^/(?P<info>.*)/comentario$', views.add_comment),
    url(r'^/(?P<info>.*)/$', views.view_info),

    url(r'^/(?P<info>.*)/like$', views.like_info),
    url(r'^/clear$', views.clear_filter),
    url('^/$', views.list_infos, name='home_info'),

]

