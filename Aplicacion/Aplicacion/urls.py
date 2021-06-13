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
from os import stat
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

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
    path('eleccionLiga/', views.eleccionLiga, name='eleccionLiga'),
    path('creacionLiga/', views.creacionLiga, name='creacionLiga'),
    path('finSesion/', views.finSesion, name='finSesion'),
    path('clasificacion/', views.clasificacion, name='clasificacion'),
    path('cambioContrasena/', views.cambiarContrasenya, name='cambioContrasenya'),
    path('cambioEmail/', views.cambiarEmail, name='cambioEmail'),
    path('cambioEquipo/', views.cambiarEquipo, name='cambioEquipo'),
    path('miEquipo/', views.miEquipo, name='miEquipo'),
    path('jugador/<id>', views.infoJugador, name='infoJugador'),
    path('mercado/', views.mercado, name='mercado'),
    path('mercado/<id>', views.jugadorAlMercado, name='JugadorAlMercado'),
    path('usuario/<nombre>', views.otrosUsuarios, name='otrosUsuarios'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('añadir_jugadores/', views.lista_jugadores_añadir, name='añadir_jugadores'),
    path('eliminar_jugadores/', views.lista_jugadores_eliminar, name='eliminar_jugadores'),
    path('eliminar/<id>', views.eliminarJugador, name='eliminarJugador'),

    url(r'^accounts/', include('registration.backends.default.urls')),
    #path('accounts/',views.include('registration.backends.default.urls')),
] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
