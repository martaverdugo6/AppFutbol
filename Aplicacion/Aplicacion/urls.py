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
from django.contrib import admin
from django.urls import path
from Aplicacion.views import inicio, sobre_nosotros,comunidad, perfil, inicioSesion
from gestionApp.views import ranking, registroUser

urlpatterns = [
    path('admin/', admin.site.urls),   #La url no tiene porque llamarse igual que la función, ni igual que el name
 	path('inicio/', inicio, name='inicio'),
 	path('sobreNosotros/', sobre_nosotros, name='about'),
 	path('ranking/', ranking, name='ranking'),
 	path('comunidad/', comunidad, name='comunidad'),
 	path('perfil/', perfil, name='perfil'),
 	path('inicioSesion/', inicioSesion, name='inicioSesion'),
 	path('registro/', registroUser, name='registro'),
]
