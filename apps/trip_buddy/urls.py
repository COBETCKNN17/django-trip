from django.conf.urls import url, include
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^show_dashboard', views.show_dashboard),
    url(r'^addtrip', views.add_trip),
    url(r'^create', views.create_trip),
    url(r'^show/(?P<id>\d+)$', views.show_trip_detail),
    url(r'^delete/(?P<id>\d+)$', views.delete_trip),
    url(r'^cancel/(?P<id>\d+)$', views.cancel_trip), 
    url(r'^join/(?P<id>\d+)$', views.join_trip), 
]