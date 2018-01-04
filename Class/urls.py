from django.conf.urls import url,include
from django.contrib import admin
from . import views

appname='Class'
urlpatterns = [
    url(r'^addClass/',views.addClass,name="addClass"),
]