from random import randint
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from gestionApp.models import Usuario, Jugador, Plantilla, Liga, Mercado
from gestionApp.forms import form_alta_usuario, form_login_usuario, form_contact, form_liga
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


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

			asignarJugadores(username)

			return HttpResponseRedirect('/eleccionLiga')	#si se ha rellenado el formulario con exito vamos a form_liga
		return render(request, "form_alta_usuario.html", {'form':form,})
	else:
		form = form_alta_usuario()
		return render(request, "form_alta_usuario.html", {'form':form,})	#si no se ha rellenado el formulario (primera vez que entramos), cargamos la pag de formulario


def inicioSesion(request):
	username = request.session.get("user_logeado")
	if username:
		return HttpResponseRedirect('/inicio')
	else:
		if request.method =='POST':					#si se envia el formulario
			form = form_login_usuario(request.POST or None)
			username = request.POST.get('username')
			password = request.POST.get('password')
			my_user = Usuario.objects.filter(username=username,password=password)
			#print(my_user)
			if my_user:
				request.session["user_logeado"] = username
				
				return HttpResponseRedirect('/inicio')
				
				
			else:
				aviso = "Los campos no son correctos. Inténtelo de nuevo"
				return render(request, "inicio_sesion.html", {'form':form,'aviso':aviso})

		else:
			form = form_login_usuario()
			return render(request, "inicio_sesion.html", {'form':form,})
		

def inicio(request):
	username = request.session.get("user_logeado")
	if username:
		return render(request, "inicio.html", {'username':username})
	else:
		return HttpResponseRedirect('/inicioSesion')

def sobre_nosotros(request):
	username = request.session.get("user_logeado")
	if username:
		return render(request, "sobre_nosotros.html", {'username':username})
	else:
		return HttpResponseRedirect('/inicioSesion')
	

def liga(request):
	username = request.session.get("user_logeado")
	if username:
		return render(request, "liga.html", {'username':username})
	else:
		return HttpResponseRedirect('/inicioSesion')

def perfil(request):
	username = request.session.get("user_logeado")
	if username:
		return render(request, "perfil_user.html", {'username':username})
	else:
		return HttpResponseRedirect('/inicioSesion')


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
		username = request.session.get("user_logeado")			#nombre del user registrado
		my_user = Usuario.objects.filter(username=username)		#objeto Usuario con nombre username
		#print(username)
		if request.method=="POST":
			form=form_liga(request.POST)
			nombreLiga = request.POST.get('nombre')
			#print(nombreLiga)
			liga_bd = Liga.objects.filter(nombre=nombreLiga)
			print(liga_bd)
			if liga_bd:
				my_form = form.save(commit=False)
				my_form.usuario = my_user.first()
				my_form.save()

				return HttpResponseRedirect('/inicio')
			return render(request, "eleccion_liga.html", {'form':form,'username':username})
		else:
			form=form_liga()
			return render(request, "eleccion_liga.html", {'form':form,'username':username})


def creacionLiga(request):
	username = request.session["user_logeado"]		#nombre del user registrado
	my_user = Usuario.objects.filter(username=username)

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
	username = request.session.get("user_logeado")
	if username:
		del request.session["user_logeado"]
		return render(request, "fin_sesion.html")
	else:
		return HttpResponseRedirect('/inicioSesion')
	
def clasificacion(request):
	username = request.session.get("user_logeado")			#usuario logueado
	my_liga = Liga.objects.filter(usuario=username)			#objeto liga del usuario logueado
	nombre_liga = my_liga.first().nombre					#nombre de la liga del usuario logueado 
	lista = Liga.objects.filter(nombre=nombre_liga)			#todos los objetos con el nombre de liga
	lista_usuarios = []

	for elementos in lista:
		lista_usuarios.append(elementos.usuario)			#añado a una lista los usuarios que están en la liga del user logueado

	print(lista_usuarios)
	return render(request, "clasificacion.html",{'lista':lista_usuarios, 'username':username})


def asignarJugadores(request):
	my_user = Usuario.objects.filter(username=request)			#Obtenemos el objeto con nombre pasado por param
	lista_jugadores = Jugador.objects.all()

	for i in [0,1,2,3,4]:
		my_jug = lista_jugadores[randint(0,len(lista_jugadores)-1)]	#Obtiene un jugador al azar
		my_plantilla=Plantilla(seleccion='NO_SELECCIONADO', usuario=my_user.first() ,jugador=my_jug)
		my_plantilla.save()

	
def ranking(request):
	#username = request.session.get("user_logeado")
	
	lista_usuarios=Usuario.objects.all().order_by("-puntuacion")[0:5]
	return render(request, "ranking.html", locals())