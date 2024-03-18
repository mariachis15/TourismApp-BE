from django.urls import path, re_path
from TurismApp import views


urlpatterns = [
    re_path(r'^destination$', views.destinationApi),
    re_path(r'destination/([0-9]+)$', views.destinationApi),
    re_path(r'^login$', views.loginApi),
    re_path(r'^register$', views.registerApi)
]