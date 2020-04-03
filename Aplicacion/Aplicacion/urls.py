"""Aplicacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Aplicacion import views
from gestionApp import views

urlpatterns = [
    path('admin/', admin.site.urls),   #La url no tiene porque llamarse igual que la función, ni igual que el name
 	path('inicio/', views.inicio, name='inicio'),
 	path('sobreNosotros/', views.sobre_nosotros, name='about'),
 	path('ranking/', views.ranking, name='ranking'),
 	path('liga/', views.liga, name='liga'),
 	path('perfil/', views.perfil, name='perfil'),
 	path('inicioSesion/', views.inicioSesion, name='inicioSesion'),
 	path('registro/', views.registroUser, name='registro'),
    path('contacto/', views.contacto, name='contacto'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #path('accounts/',views.include('registration.backends.default.urls')),
]
