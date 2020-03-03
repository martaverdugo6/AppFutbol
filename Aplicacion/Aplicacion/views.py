from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def inicio(request):

	return render(request, "inicio.html")

def sobre_nosotros(request):

	return render(request, "sobre_nosotros.html")


def liga(request):

	return render(request, "liga.html")

def perfil(request):

	return render(request, "perfil_user.html")

