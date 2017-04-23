from django.conf.urls import url
import views

urlpatterns = [
    url(r'^/add_actividad/$', views.add_actividad),
    url(r'^/delete_actividad', views.delete_actividad),
    url(r'^/(?P<actividad>.*)/like$', views.like_actividad),
    url(r'^/(?P<actividad>.*)/comentario/$', views.add_comment),
    url(r'^/(?P<actividad>.*)/registrate/$', views.registrate),
    url(r'^/(?P<actividad>.*)/add_miniactividad/$', views.add_miniactividad),
    url(r'^/(?P<actividad>.*)/$', views.view_actividad),
    url(r'^/(?P<actividad>.*)/download$', views.download),
    url(r'^/clear$', views.clear_filter),
    url("^/$", views.list_actividades, name="home_propuestas"),
]
