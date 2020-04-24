from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from gestionApp.models import usuario, jugador, plantilla, liga, mercado
from gestionApp.forms import form_alta_usuario, form_login_usuario, form_contact, form_liga
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def ranking(request):
	lista_usuarios=usuario.objects.all().order_by("-puntuacion")[0:5]
	return render(request, "ranking.html", locals())

def registroUser(request):
	if request.method =='POST':									#si se envia el formulario
		form = form_alta_usuario(request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			request.session["user_logeado"] = username

			my_form = form.save(commit=False)
			my_form.puntuacion = 0
			my_form.presupuesto = 200000
			my_form.save()

			return HttpResponseRedirect('/eleccionLiga')	#si se ha rellenado el formulario con exito vamos a form_liga
		return render(request, "form_alta_usuario.html", {'form':form,})
	else:
		form = form_alta_usuario()
		return render(request, "form_alta_usuario.html", {'form':form,})	#si no se ha rellenado el formulario (primera vez que entramos), cargamos la pag de formulario


def inicioSesion(request):
	if request.method =='POST':					#si se envia el formulario
		form = form_login_usuario(request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')
		my_user = usuario.objects.filter(username=username,password=password)
		#print(my_user)
		if my_user:
			request.session["user_logeado"] = username
			
			return HttpResponseRedirect('/inicio', {'username':username})
			
			
		else:
			aviso = "Los campos no son correctos. Inténtelo de nuevo"
			return render(request, "inicio_sesion.html", {'form':form,'aviso':aviso})

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

def contacto(request):

	if request.method=="POST":
		my_form = form_contact(request.POST)
		if my_form.is_valid():
			inf_form = my_form.cleaned_data

			send_mail(inf_form['asunto'],inf_form['mensaje'],
												inf_form.get('email',''),['martaverdugo06@gmail.com'],)
			
			return render(request, "mensaje_enviado.html")

	else:
		my_form = form_contact()

	return render(request, "contacto.html", {'form':my_form})


def eleccionLiga(request):
	username = request.session["user_logeado"]		#nombre del user registrado
	#print(username)
	if request.method=="POST":
		form=form_liga(request.POST)
		if form.is_valid():
			nombreLiga = request.POST.get('nombre')
			#print(nombreLiga)
			liga_bd = liga.objects.all()
			print(liga_bd)
			#if liga_bd:
			#	my_form = form.save(commit=False)
			#	my_form.usuario = my_user
			#	my_form.save()

			#	return HttpResponseRedirect('/inicio',{'nombre':username,})
		return render(request, "eleccion_liga.html", {'form':form,'username':username})
	else:
		form=form_liga()
		return render(request, "eleccion_liga.html", {'form':form,'username':username})


def creacionLiga(request):
	username = request.session["user_logeado"]		#nombre del user registrado
	my_user = usuario.objects.filter(username=username)

	if request.method=="POST":
		form=form_liga(request.POST)
		if form.is_valid():
			nombreLiga = request.POST.get('nombre')
			#print(nombreLiga)
			my_form = form.save(commit=False)
			my_form.usuario = my_user.first()
			my_form.save()

			return HttpResponseRedirect('/inicio',{'username':username})
		return render(request, "creacion_liga.html", {'form':form})	
	else:
		form=form_liga()
		return render(request, "creacion_liga.html", {'form':form})	
	

def finSesion(request):
	del request.session["user_logeado"]
	return render(request, "fin_sesion.html")