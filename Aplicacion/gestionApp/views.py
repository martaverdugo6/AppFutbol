from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from gestionApp.models import usuario
from gestionApp.forms import form_alta_usuario, form_login_usuario
from django.template import loader

# Create your views here.

def ranking(request):
	lista_usuarios=usuario.objects.all().order_by("-puntuacion")[0:5]
	return render(request, "ranking.html", locals())

def registroUser(request):
	if request.method =='POST':	#si se envia el formulario
		form = form_alta_usuario(request.POST)
		if form.is_valid():
			my_form = form.save(commit=False)
			my_form.puntuacion = 0
			my_form.presupuesto = 200000
			my_form.save()

		#return HttpResponseRedirect('/perfil')
	else:
		form = form_alta_usuario()
	return render(request, "form_alta_usuario.html", {'form':form,})

def inicioSesion(request):
	if request.method =='POST':	#si se envia el formulario
		form = form_login_usuario(request.POST)
		if form.is_valid():
			my_form = form.save(commit=False)
			my_form.save()

		#return HttpResponseRedirect('/perfil')
	else:
		form = form_login_usuario()
	return render(request, "inicio_sesion.html", {'form':form,})

def inicio(request):

	return render(request, "inicio.html")

def sobre_nosotros(request):

	return render(request, "sobre_nosotros.html")


def liga(request):

	return render(request, "liga.html")

def perfil(request):

	return render(request, "perfil_user.html")
