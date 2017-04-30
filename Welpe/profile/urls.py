from __future__ import unicode_literals
from django.conf.urls import url
from Welpe.profile import views

urlpatterns = [
    url(r'^/(?P<user>.*)/$', views.view_profile),
    url(r'^/(?P<user>.*)/send$', views.send_message),
]
