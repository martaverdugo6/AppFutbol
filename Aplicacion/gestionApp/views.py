from random import randint
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from gestionApp.models import Usuario, Jugador, Plantilla, Liga, Mercado, Puja
from gestionApp.forms import form_alta_usuario, form_login_usuario, form_liga, form_cambio_password
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime						#para añadir la hora actual
import datetime
from django.utils import timezone

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
				request.session["user_logeado"] = username			#guarda el nombre en variable global
				puntuacionUsuario(username)						#calcular la puntuación del user a partir de la de sus jug.
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
		puntuacionUsuario(username)
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
	my_user = Usuario.objects.filter(username=username) 
	my_liga = Liga.objects.filter(usuario__in=my_user)
	if username:
		return render(request, "liga.html", {'username':username, 'my_liga':my_liga.first()})
	else:
		return HttpResponseRedirect('/inicioSesion')

def perfil(request):
	username = request.session.get("user_logeado")
	if username:
		my_user = Usuario.objects.filter(username=username)
		return render(request, "perfil_user.html", {'username':username,'my_user':my_user.first()})
	else:
		return HttpResponseRedirect('/inicioSesion')

def cambiarContrasenya(request):
	username = request.session.get("user_logeado")
	form=form_cambio_password()
	if username:
		if request.method =='POST':	
			form = form_cambio_password(request.POST)
			if form.is_valid():
				password = request.POST.get('Contraseña_actual')
				new_password = request.POST.get('Nueva_contraseña')
				my_user = Usuario.objects.filter(username=username,password=password)
				msgFracaso="La contraseña actual no es correcta"
				if my_user:
					usuario = my_user.first()
					usuario.password=new_password
					usuario.save()
					form=form_cambio_password()
					msgExito="Contraseña cambiada con exito"
					return render(request, "cambio_password.html",{'username':username,'form':form,'msgExito':msgExito})
				else:
					return render(request, "cambio_password.html",{'username':username,'form':form,'msgFracaso':msgFracaso})
		return render(request, "cambio_password.html",{'username':username,'form':form})
	else:
		return HttpResponseRedirect('/inicioSesion')


def eleccionLiga(request):
		username = request.session.get("user_logeado")			#nombre del user registrado
		my_user = Usuario.objects.filter(username=username)		#objeto Usuario con nombre username
		#print(username)
		if request.method=="POST":
			form=form_liga(request.POST)
			nombreLiga = request.POST.get('nombre')
			#print(nombreLiga)
			liga_bd = Liga.objects.filter(nombre=nombreLiga)
			if len(liga_bd) >= 10:
				msgLigaCompleta = "Lo sentimos. Esta liga ya está completa."
			elif liga_bd:
				
				my_form = form.save(commit=False)
				my_form.usuario = my_user.first()
				my_form.save()

				asignarJugadores(username)

				return HttpResponseRedirect('/inicio')
			return render(request, "eleccion_liga.html", {'form':form,'my_username':username, 'msg':msgLigaCompleta})
		else:
			form=form_liga()
			return render(request, "eleccion_liga.html", {'form':form,'my_username':username})


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

			asignarJugadores(username)

			return HttpResponseRedirect('/inicio',{'username':username})
		return render(request, "creacion_liga.html", {'form':form})	
	else:
		form=form_liga()
		return render(request, "creacion_liga.html", {'form':form})	
	
def asignarJugadores(request):
	my_user = Usuario.objects.filter(username=request)			#Obtenemos el objeto con nombre pasado por param
	lista_jugadores = Jugador.objects.all()
	liga_user = Liga.objects.filter(usuario__in=my_user)
	nombre_liga = liga_user.first().nombre
	lista_users = Liga.objects.filter(nombre=nombre_liga)
	users = []
	for i in lista_users:
		users.append(i.usuario)			#lista de jugadores de la misma liga que el nuevo jugador	
	
	jugadores_liga= []
	
	for j in users:
		filas_plantilla = Plantilla.objects.filter(usuario=j)
		for k in filas_plantilla:
			jugadores_liga.append(k.jugador)		#jugadores ya asignados a otros usuarios de la misma liga
			
	while len(Plantilla.objects.filter(usuario=my_user.first()))+1 < 16 : 
		jugador_random = lista_jugadores[randint(0,len(lista_jugadores)-1)]	#Obtiene un jugador al azar
		jug_repetido = Plantilla.objects.filter(usuario=my_user.first() ,jugador=jugador_random)
		jug_asignado = []
		for i in jugadores_liga:				#compruebo que el jugador random no esta entre los jugadores de otros usuarios
			if i==jugador_random:
				jug_asignado.append(i)				
				
		if (len(jug_repetido)==0 and len(jug_asignado)==0):		#solo inserto la asignacion si el jugador no ha sido asignado anteriormente
			my_plantilla=Plantilla(seleccion='NO SELECCIONADO', usuario=my_user.first() ,jugador=jugador_random)
			my_plantilla.save()

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
	
	return render(request, "clasificacion.html",{'username':username,'nombre_liga':nombre_liga,'lista_usuarios':lista_usuarios})

def miEquipo(request):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.get(username=username)
	if username:
		my_plantilla = Plantilla.objects.filter(usuario=my_user)
		return render(request, "mi_equipo.html",{'my_user':my_user,'username':username, 'my_plantilla':my_plantilla})
	else:
		return HttpResponseRedirect('/inicioSesion')


def puntuacionUsuario(request):
	my_user = Usuario.objects.filter(username=request)
	plantilla_user = Plantilla.objects.filter(usuario__in=my_user)
	puntuacion = 0
	for jug_user_selec in plantilla_user:
		jugador = jug_user_selec.jugador
		puntuacion += jugador.puntuacion

	user_update = my_user.first()
	user_update.puntuacion = puntuacion
	user_update.save()	

def fuera_del_mercado():
	obj_mercado = Mercado.objects.all()
	ahora = timezone.now()
	for i in obj_mercado:
		caducidadDelJug = i.fecha_increso + datetime.timedelta(days=2)		#El jugador sale del marcado 2 días después de ingresar
		if ahora > caducidadDelJug:
			jugadorOut = Mercado.objects.get(liga_mercado=i.liga_mercado,jugador_mercado=i.jugador_mercado)
			jugadorOut.delete()

	
def mercado(request):
	username = request.session.get("user_logeado")
	nombre_liga = Liga.objects.filter(usuario=username).first().nombre			#objeto liga del usuario logueado								
	if username:
		fuera_del_mercado()
		my_user = Usuario.objects.get(username=username)						#usuario con nombre username
		users = Liga.objects.filter(nombre=nombre_liga)							#lista de ligas con nombre de la liga de my_user
		jugadores_en_el_mercado = []
		for usuarios in users:
			nombre_usuario = usuarios.usuario
			la_liga = Liga.objects.filter(usuario=nombre_usuario)
			aux = Mercado.objects.filter(liga_mercado__in=la_liga)
			for i in aux:
				jugadores_en_el_mercado.append(i)			#filas del model mercado
				#print(jugadores_en_el_mercado)
			
		if request.method=="POST":
			if request.POST.get('puja'):
				puja = request.POST.get('puja')
				id_jugador = request.POST.get('idJugador')
				jugador = Jugador.objects.get(id=id_jugador)

				puja_repe = Puja.objects.filter(pujador=my_user,jugador=jugador,cantidad=puja)		#compruebo que el jugador no repite la puja
				if len(puja_repe) == 0:
					obj = Puja(pujador=my_user, jugador=jugador,cantidad=puja,liga=la_liga.first())
					obj.save()
					del puja

		pujas = []
		for jug in jugadores_en_el_mercado:
			if Puja.objects.filter(jugador=jug.jugador_mercado):
				pujas_aux = Puja.objects.filter(jugador=jug.jugador_mercado).order_by("-cantidad")[0]
				pujas.append(pujas_aux)
		
		return render(request, "mercado.html", {'username':username,'jugadores_en_el_mercado':jugadores_en_el_mercado,'nombre_liga':nombre_liga,'pujas':pujas})
	else:
		return HttpResponseRedirect('/inicioSesion')

def jugadorAlMercado(request,id):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.filter(username=username)
	my_liga = Liga.objects.filter(usuario__in=my_user)
	#print(my_liga)
	if username:
		jugadorAñadido=False
		mi_jugador = Jugador.objects.get(id=id)
		#print(mi_jugador)
		jugadorRepetido = Mercado.objects.filter(liga_mercado__in=my_liga,jugador_mercado=mi_jugador)
		print(jugadorRepetido)
	
		if request.method=="POST":
			mensaje_de_error="El jugador ya está añadido, no puede añadirlo de nuevo."
			if (len(jugadorRepetido) == 0):
				obj = Mercado(liga_mercado=my_liga.first(),jugador_mercado=mi_jugador,fecha_increso=datetime.datetime.utcnow())
				obj.save()
				jugadorAñadido=True
			return render(request, "jugador_al_mercado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorAñadido':jugadorAñadido,'mensaje_de_error':mensaje_de_error})
		return render(request, "jugador_al_mercado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorAñadido':jugadorAñadido})
	else:
		return HttpResponseRedirect('/inicioSesion')

	
def infoJugador(request,id):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.filter(username=username)
	if username:
		mi_jugador = Jugador.objects.get(id=id)
		#print(mi_jugador)
		propietario = Plantilla.objects.filter(jugador=mi_jugador).first().usuario
		#print(propietario)
		return render(request, "info_jugador.html", {'username':username,'mi_jugador':mi_jugador,'propietario':propietario})
	else:
		return HttpResponseRedirect('/inicioSesion')
	
def otrosUsuarios(request, nombre):
	username = request.session.get("user_logeado")
	if username:
		my_user = Usuario.objects.filter(username=nombre).first()
		#print(my_user)
		return render(request, "otros_usuarios.html",{'username':username,'my_user':my_user})
	else:
		return HttpResponseRedirect('/inicioSesion')




def ranking(request):
	username = request.session.get("user_logeado")
	#asignarJugadores(username)
	#lista_usuarios=Usuario.objects.all().order_by("-puntuacion")[0:5]
	
	pasadoManana = timezone.now() + datetime.timedelta(days=2)
	print(pasadoManana)

	obj_mercado = Mercado.objects.all()
	ahora = timezone.now()
	for i in obj_mercado:
		fecha = ahora - i.fecha_increso
		print(fecha)
	return render(request, "ranking.html", locals())
	