from django.shortcuts import render

# Create your views here.
from random import randint
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from gestionApp.models import Usuario, Jugador, Plantilla, Liga, Mercado, Puja, Jornada, Opciones
from gestionApp.forms import form_alta_usuario, form_login_usuario, form_liga, form_cambio_password, form_cambio_email, form_cambio_equipo
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime						#para añadir la hora actual
import datetime
from django.utils import timezone					#para añadir la hora actual

# Create your views here.


def registroUser(request):
	if request.method =='POST':									#si se envia el formulario
		form = form_alta_usuario(request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			request.session["user_logeado"] = username
			presupuesto_inicial = Opciones.objects.get(id=1).presupuesto_de_inicio

			my_form = form.save(commit=False)
			my_form.puntuacion = 0
			my_form.presupuesto = presupuesto_inicial
			my_form.save()

			return HttpResponseRedirect('/eleccionLiga')	#si se ha rellenado el formulario con exito vamos a form_liga
		return render(request, "form_alta_usuario.html", {'form':form,})
	else:
		form = form_alta_usuario()
		return render(request, "form_alta_usuario.html", {'form':form,})	#si no se ha rellenado el formulario (primera vez que entramos), cargamos la pag de formulario


def inicioSesion(request):
	username = request.session.get("user_logeado")
	
	activar_sumar_puntuacion = Opciones.objects.filter(id=1, sumar_puntos_jorn = 'SI')
	if activar_sumar_puntuacion:
		puntuacionUsuarioJornada(request)
	
	
	if username:
		return HttpResponseRedirect('/inicio')
	else:
		if request.method =='POST':									#si se envia el formulario
			form = form_login_usuario(request.POST or None)
			username = request.POST.get('username')
			password = request.POST.get('password')
			my_user = Usuario.objects.filter(username=username,password=password)
			#print(my_user)
			if my_user:
				request.session["user_logeado"] = username			#guarda el nombre en variable global
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

def ayuda(request):
	username = request.session.get("user_logeado")
	if username:
		return render(request, "ayuda.html", {'username':username})
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
	opcionesPulsado = False
	if username:
		if request.method =='POST':
			opciones = request.POST.get('opciones')
			if opciones == "salir_opciones":
				opcionesPulsado = False
			else:
				opcionesPulsado = True

		my_user = Usuario.objects.filter(username=username)
		return render(request, "perfil_user.html", {'username':username,'my_user':my_user.first(), 'opcionesPulsado':opcionesPulsado})
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

def cambiarEmail(request):
	username = request.session.get("user_logeado")
	form=form_cambio_email()
	if username:
		if request.method =='POST':	
			form = form_cambio_email(request.POST)
			if form.is_valid():
				email = request.POST.get('Email_actual')
				new_email = request.POST.get('Nuevo_email')
				my_user = Usuario.objects.filter(username=username,email=email)
				msgFracaso="El email actual no es correcto"
				if my_user:
					usuario = my_user.first()
					usuario.email=new_email
					usuario.save()
					form=form_cambio_email()
					msgExito="Email cambiado con exito"
					return render(request, "cambio_email.html",{'username':username,'form':form,'msgExito':msgExito})
				else:
					return render(request, "cambio_email.html",{'username':username,'form':form,'msgFracaso':msgFracaso})
		return render(request, "cambio_email.html",{'username':username,'form':form})
	else:
		return HttpResponseRedirect('/inicioSesion')

def cambiarEquipo(request):
	username = request.session.get("user_logeado")
	form=form_cambio_equipo()
	if username:
		if request.method =='POST':	
			form = form_cambio_equipo(request.POST)
			if form.is_valid():
				equipo = request.POST.get('Nombre_actual_del_equipo')
				new_equipo = request.POST.get('Nuevo_nombre_para_el_equipo')
				my_user = Usuario.objects.filter(username=username,mi_equipo=equipo)
				msgFracaso="El nombre del equipo no es correcto"
				if my_user:
					usuario = my_user.first()
					usuario.mi_equipo=new_equipo
					usuario.save()
					form=form_cambio_equipo()
					msgExito="Nombre del equipo cambiado con exito"
					return render(request, "cambio_equipo.html",{'username':username,'form':form,'msgExito':msgExito})
				else:
					return render(request, "cambio_equipo.html",{'username':username,'form':form,'msgFracaso':msgFracaso})
		return render(request, "cambio_equipo.html",{'username':username,'form':form})
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
			if len(liga_bd) >= Opciones.objects.get(id=1).max_num_usuarios_liga:
				msg = "Lo sentimos. Esta liga ya está completa."
			elif len(liga_bd) ==0:
				msg = "Lo sentimos. No existe ninguna liga con ese nombre."
			elif liga_bd:
				
				my_form = form.save(commit=False)
				my_form.usuario = my_user.first()
				my_form.save()

				asignarJugadores(username)

				return HttpResponseRedirect('/inicio')
			return render(request, "eleccion_liga.html", {'form':form,'my_username':username, 'msg':msg})
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
			if len(Liga.objects.filter(nombre=nombreLiga))==0:		#solo creamos la liga si no existe ninguna con ese nombre ya creada
				my_form = form.save(commit=False)
				my_form.usuario = my_user.first()
				my_form.save()

				asignarJugadores(username)

				return HttpResponseRedirect('/inicio',{'username':username})
			else:
				msg = "El nombre de la liga ya existe. Pruebe con otro"	
				return render(request, "creacion_liga.html", {'form':form, 'msg':msg})	
			
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

	numero_jug_inicio = Opciones.objects.get(id=1).num_jug_plant_inicio
	while len(Plantilla.objects.filter(usuario=my_user.first())) < numero_jug_inicio: 
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
	mensaje_de_error = False
	if username:
		if request.method=="POST":
			id_jug = request.POST.get('jug')
			this_jugador = Jugador.objects.filter(id = id_jug).first()
			jug_plantilla = Plantilla.objects.filter(usuario = my_user, jugador = this_jugador).first()
			if jug_plantilla.seleccion == 'SELECCIONADO':			#Si jugador está seleccionado, se pone a No seleccionado
				jug_plantilla.seleccion = 'NO SELECCIONADO'
				jug_plantilla.save()
			else:
				if len(Plantilla.objects.filter(usuario=my_user, seleccion='SELECCIONADO')) >= 11:
					mensaje_de_error = True
				else:
					jug_plantilla.seleccion = 'SELECCIONADO'
					jug_plantilla.save()

		my_plantilla_no_seleccionada = Plantilla.objects.filter(usuario=my_user, seleccion='NO SELECCIONADO')
		total_no_selec = len(Plantilla.objects.filter(usuario=my_user, seleccion='NO SELECCIONADO'))
		my_plantilla_seleccionada = Plantilla.objects.filter(usuario=my_user, seleccion='SELECCIONADO')
		total_selec = len(Plantilla.objects.filter(usuario=my_user, seleccion='SELECCIONADO'))

		ultima_jornada = request.session.get("numero_jornada")		#variable global inicializada en inicioSesion
		jugadores_de_la_jorn = Jornada.objects.filter(numero_jornada=ultima_jornada)		#filas de la jorn que este en la variable global

		return render(request, "mi_equipo.html",{'my_user':my_user,'username':username, 'my_plantilla_no_seleccionada':my_plantilla_no_seleccionada, 'my_plantilla_seleccionada':my_plantilla_seleccionada,'mensaje_de_error':mensaje_de_error,'total_no_selec':total_no_selec,'total_selec':total_selec, 'jugadores_de_la_jorn':jugadores_de_la_jorn})
	else:
		return HttpResponseRedirect('/inicioSesion')


def puntuacionUsuarioJornada(request):
	numero_jorn = Opciones.objects.get(id=1).ultima_jornada
	jornada_a_sumar = Jornada.objects.filter(numero_jornada = numero_jorn, jornada_sumada = 'NO')
	if jornada_a_sumar:			#si todas las filas de la clase jornada han sido sumadas ya, esta función no hace nada
		usuarios_app = Usuario.objects.all()
		#print(usuarios_app)
		for i in usuarios_app:
			print(i)
			jugadores_selec = Plantilla.objects.filter(usuario=i, seleccion='SELECCIONADO')		#cada jugador_selec es una fila de plantillas
			for j in jugadores_selec:
				jug_en_jorn = Jornada.objects.filter(jugador=j.jugador, jornada_sumada = 'NO')
				if jug_en_jorn:
					for x in jug_en_jorn:
						i.puntuacion = i.puntuacion + x.puntos
						i.save()
						x.jornada_sumada = 'SI'
						x.save()

		jug_no_selc_x_nadie = Jornada.objects.filter(jornada_sumada = 'NO')	
		if jug_no_selc_x_nadie:
			for n in jug_no_selc_x_nadie:
				n.jornada_sumada = 'SI'
				n.save()				
	

def fuera_del_mercado(username):
	liga_user = Liga.objects.filter(usuario=username).first()				#liga del usuario logueado
	obj_mercado = Mercado.objects.all()
	ahora = timezone.now()
	for i in obj_mercado:
		caducidadDelJug = i.fecha_ingreso + datetime.timedelta(days=2)		#El jugador sale del marcado 2 días después de ingresar
		if ahora > caducidadDelJug:											#Si la fecha actual es posterior a la de "caducidad" del jugador en el mercado
			jugadorOutMercado = Mercado.objects.get(liga=i.liga,jugador=i.jugador)
			my_jugador = jugadorOutMercado.jugador

			existe_puja = Puja.objects.filter(jugador=my_jugador)		#Comprobamos que al menos haya una puja realizada por el jugador 
			if existe_puja:			#si nadie ha pujado por el jug solo lo eliminamos del mercado, sin hacer el cambio de propietario y sin cambiar los presupuestos de los usuarios
				puja_superior = Puja.objects.filter(jugador=my_jugador).order_by("-cantidad")[0]	#ya sabemos que al menos una puja hay, cogemos la mayor en caso de haber varias
				lineas_clase_liga = Liga.objects.filter(nombre=i.nombre)		#busco los usuarios de la misma liga que el jugador que queremos eliminar del mercado
				
				for j in lineas_clase_liga:				#recorremos todos los usuarios para ver cual tiene como jugador el que acabamos de vender
					quitar_de_plantilla = Plantilla.objects.filter(usuario = j.usuario, jugador = my_jugador)
					if quitar_de_plantilla:
						quitar_de_plantilla.delete()
						j.usuario.presupuesto = j.usuario.presupuesto + puja_superior.cantidad			#sumar el dinero de la venta del jugador
						j.usuario.save()


				pujador_win = puja_superior.pujador
				pujador_win.presupuesto = pujador_win.presupuesto - puja_superior.cantidad		#Quitarle el dinero que le ha costado el jugador de su presupuesto
				pujador_win.save()
				añadir_a_plantilla= Plantilla(seleccion='NO SELECCIONADO', usuario=pujador_win ,jugador=my_jugador)	#asignamos el jugador a su nuevo usuario
				añadir_a_plantilla.save()	

			usuarios_pujantes = Liga.objects.filter(nombre = i.liga.nombre)
			for x in usuarios_pujantes:					#cada x una fila de la liga del jug que se va a eliminar
				puja_por_jug = Puja.objects.filter(pujador = x.usuario, jugador = my_jugador)
				puja_por_jug.delete()
			
			jugadorOutMercado.delete()

	
def mercado(request):
	username = request.session.get("user_logeado")
	nombre_liga = Liga.objects.filter(usuario=username).first().nombre			#objeto liga del usuario logueado								
	if username:
		fuera_del_mercado(username)
		my_user = Usuario.objects.get(username=username)						#usuario con nombre username
		users = Liga.objects.filter(nombre=nombre_liga)							#lista de ligas con nombre de la liga de my_user
		jugadores_en_el_mercado = []
		j = 0
		for usuarios in users:
			nombre_usuario = usuarios.usuario
			la_liga = Liga.objects.filter(usuario=nombre_usuario)
			aux = Mercado.objects.filter(liga__in=la_liga)
			for i in aux:
				jugadores_en_el_mercado.append(i)			#cada i es una filasa de la clase mercado filtrada por la liga del user logueado
				#print(jugadores_en_el_mercado)
				#ahora = timezone.now() #caducidadDelJug = i.fecha_ingreso + datetime.timedelta(days=2)
				#caducidad_jug = (i.fecha_ingreso + datetime.timedelta(days=2)) - ahora		#caducidad_jug guarda el tiempo que queda para que el jugador salga del mercado
				#dic_jug_caducidad = {}
				#dias = caducidad_jug.days
				#minutos =  caducidad_jug.seconds // 60
				#horas = caducidad_jug.seconds // 3600
				#fecha_cad = []								#creo lista para añadir día, hora y minuto
				#fecha_cad.append(dias)
				#fecha_cad.append(horas)
				#fecha_cad.append(minutos)
				#print(j)
				#dic_jug_caducidad[j] = fecha_cad
				#j=j+1
				#print(j)
				#print(dic_jug_caducidad)
				
				
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
			if Puja.objects.filter(jugador=jug.jugador):
				pujas_aux = Puja.objects.filter(jugador=jug.jugador).order_by("-cantidad")[0]
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
		jugadorRepetido = Mercado.objects.filter(liga__in=my_liga,jugador=mi_jugador)
		print(jugadorRepetido)
	
		if request.method=="POST":
			mensaje_de_error="El jugador ya está añadido, no puede añadirlo de nuevo."
			if (len(jugadorRepetido) == 0):
				obj = Mercado(liga=my_liga.first(),jugador=mi_jugador,fecha_ingreso=datetime.datetime.utcnow())
				obj.save()
				jugadorAñadido=True
			return render(request, "jugador_al_mercado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorAñadido':jugadorAñadido,'mensaje_de_error':mensaje_de_error})
		return render(request, "jugador_al_mercado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorAñadido':jugadorAñadido})
	else:
		return HttpResponseRedirect('/inicioSesion')

	
def infoJugador(request,id):				#Vista cuando pulsamos en el nombre de un jugador
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
	
def otrosUsuarios(request, nombre):			#Vista del perfil de otro usuario que no es el que está logueado actualmente
	username = request.session.get("user_logeado")
	if username:
		my_user = Usuario.objects.filter(username=nombre).first()
		#print(my_user)
		return render(request, "otros_usuarios.html",{'username':username,'my_user':my_user})
	else:
		return HttpResponseRedirect('/inicioSesion')

def jugadores(request):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.get(username=username)
	if username:
		my_plantilla = Plantilla.objects.filter(usuario=my_user)
		#print(my_plantilla)
		return render(request, "jugadores.html", {'username':username, 'my_plantilla':my_plantilla})
	else:
		return HttpResponseRedirect('/inicioSesion')


def ranking(request):
	username = request.session.get("user_logeado")
	#asignarJugadores(username)
	#lista_usuarios=Usuario.objects.all().order_by("-puntuacion")[0:5]
	
	opciones = Opciones.objects.get(id=1).max_num_usuarios_liga
	print(opciones)
	
	return render(request, "ranking.html", locals())
	



