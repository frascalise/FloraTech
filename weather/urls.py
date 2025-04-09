from django.urls import path,re_path
from django.contrib import admin
from . import views

app_name = 'meteo'
urlpatterns = [
    path('home/',views.home,name='casa base'),
    #path('forecast/',views.PrevisionDetail.as_view(),name='list'),
    path('on/',views.refresh,name='caricamento'),
    path('read/',views.fornire,name='lettura'),
    path('test/',views.LookForecast,name='prova'),
    path('model/',views.chiamata,name='chiamata')

    #path("meteo/",views.PrevisionDetail.as_view(),name="meteo")
]