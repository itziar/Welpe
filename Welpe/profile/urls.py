from django.conf.urls import url
import views

urlpatterns = [
    url(r'/signup', views.CreateUser),
    url(r'^/login', views.Autenticar),
    url(r'^/logout', views.CerrarSesion),
    url(r'^/(?P<user>.*)/$', views.view_profile),
    url(r'^/(?P<user>.*)/send$', views.send_message),

]
