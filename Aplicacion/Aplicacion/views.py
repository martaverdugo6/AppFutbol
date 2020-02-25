from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
def inicio(request):

	return render(request, "inicio.html")

def sobre_nosotros(request):

	return render(request, "sobre_nosotros.html")


def comunidad(request):

	return render(request, "comunidad.html")

def perfil(request):

	return render(request, "perfil_user.html")

def inicioSesion(request):

	return render(request, "inicio_sesion.html")
