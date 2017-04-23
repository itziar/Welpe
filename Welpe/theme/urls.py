#from django.conf.urls import patterns, url
from django.conf.urls import *

import views


urlpatterns = [
    url("^$", views.homepage, name="home"),

]

