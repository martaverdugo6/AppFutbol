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
			username = request.POST.get('Nombre_de_usuario')
			request.session["user_logeado"] = username
			email = request.POST.get('Email')
			equipo = request.POST.get('Nombre_de_equipo')
			password = request.POST.get('Contraseña')
			confirmpass = request.POST.get('Confirmar_contraseña')
			presupuesto_inicial = Opciones.objects.get(id=1).presupuesto_de_inicio
			mensaje_de_error = False

			if password == confirmpass:
				new_user = Usuario(username = username, email = email, mi_equipo = equipo, password = password, puntuacion = 0, presupuesto = presupuesto_inicial)
				new_user.save()
				return HttpResponseRedirect('/eleccionLiga')	#si se ha rellenado el formulario con exito vamos a form_liga
			else:
				mensaje_de_error = True
				return render(request, "form_alta_usuario.html", {'form':form,'mensaje_de_error':mensaje_de_error})
				
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
	my_user = Usuario.objects.filter(username=username).first()
	opcionesPulsado = False
	mensaje_de_error = False
	if username:
		if request.method =='POST':
			opciones = request.POST.get('opciones')
			if opciones == "salir_opciones":
				opcionesPulsado = False
			else:
				opcionesPulsado = True

		if my_user.presupuesto < 0:
			mensaje_de_error = True

		my_user = Usuario.objects.filter(username=username)
		return render(request, "perfil_user.html", {'username':username,'my_user':my_user.first(), 'opcionesPulsado':opcionesPulsado, 'mensaje_de_error':mensaje_de_error})
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

				return HttpResponseRedirect('/inicio',{'my_username':username})
			else:
				msg = "El nombre de la liga ya existe. Pruebe con otro"	
				return render(request, "creacion_liga.html", {'form':form, 'msg':msg, 'my_username':username})	
			
		return render(request, "creacion_liga.html", {'form':form, 'my_username':username})	
	else:
		form=form_liga()
		return render(request, "creacion_liga.html", {'form':form, 'my_username':username})	
	
def asignarJugadores(request):
	my_user = Usuario.objects.filter(username=request)			#Obtenemos el objeto con nombre pasado por param
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

	#OBLIGO A QUE AL MENOS HAYA UN PORTERO
	lista_porteros = Jugador.objects.filter(posicion='PORTERO')
	while len(Plantilla.objects.filter(usuario=my_user.first())) < 1: 
		portero_random = lista_porteros[randint(0,len(lista_porteros)-1)]			#Obtiene un portero al azar
		jug_repetido = Plantilla.objects.filter(usuario=my_user.first() ,jugador=portero_random)
		jug_asignado = []
		for i in jugadores_liga:				#compruebo que el portero random no esta entre los jugadores de otros usuarios
			if i==portero_random:
				jug_asignado.append(i)				
				
		if (len(jug_repetido)==0 and len(jug_asignado)==0):		#solo inserto la asignacion si el jugador no ha sido asignado anteriormente
			my_plantilla=Plantilla(seleccion='SELECCIONADO', usuario=my_user.first() ,jugador=portero_random)
			my_plantilla.save()

	#OBLIGO A QUE AL MENOS HAYA 4 DEFENSAS	
	lista_defensas = Jugador.objects.filter(posicion='DEFENSA')
	while len(Plantilla.objects.filter(usuario=my_user.first())) < 5: 
		defensa_random = lista_defensas[randint(0,len(lista_defensas)-1)]			#Obtiene un defensa al azar
		jug_repetido = Plantilla.objects.filter(usuario=my_user.first() ,jugador=defensa_random)
		jug_asignado = []
		for i in jugadores_liga:				#compruebo que el defensa random no esta entre los jugadores de otros usuarios
			if i==defensa_random:
				jug_asignado.append(i)				
				
		if (len(jug_repetido)==0 and len(jug_asignado)==0):		#solo inserto la asignacion si el jugador no ha sido asignado anteriormente
			my_plantilla=Plantilla(seleccion='SELECCIONADO', usuario=my_user.first() ,jugador=defensa_random)
			my_plantilla.save()

	#OBLIGO A QUE AL MENOS HAYA 4 CENTROCAMPISTAS	
	lista_centrocampistas = Jugador.objects.filter(posicion='CENTROCAMPISTA')
	while len(Plantilla.objects.filter(usuario=my_user.first())) < 9: 
		centrocampista_random = lista_centrocampistas[randint(0,len(lista_centrocampistas)-1)]			#Obtiene un defensa al azar
		jug_repetido = Plantilla.objects.filter(usuario=my_user.first() ,jugador=centrocampista_random)
		jug_asignado = []
		for i in jugadores_liga:				#compruebo que el centrocampista random no esta entre los jugadores de otros usuarios
			if i==centrocampista_random:
				jug_asignado.append(i)				
				
		if (len(jug_repetido)==0 and len(jug_asignado)==0):		#solo inserto la asignacion si el jugador no ha sido asignado anteriormente
			my_plantilla=Plantilla(seleccion='SELECCIONADO', usuario=my_user.first() ,jugador=centrocampista_random)
			my_plantilla.save()

	#OBLIGO A QUE AL MENOS HAYA 2 DELANTEROS	
	lista_delanteros = Jugador.objects.filter(posicion='DELANTERO')
	while len(Plantilla.objects.filter(usuario=my_user.first())) < 11: 
		delantero_random = lista_delanteros[randint(0,len(lista_delanteros)-1)]			#Obtiene un delantero al azar
		jug_repetido = Plantilla.objects.filter(usuario=my_user.first() ,jugador=delantero_random)
		jug_asignado = []
		for i in jugadores_liga:				#compruebo que el delantero random no esta entre los jugadores de otros usuarios
			if i==delantero_random:
				jug_asignado.append(i)				
				
		if (len(jug_repetido)==0 and len(jug_asignado)==0):		#solo inserto la asignacion si el jugador no ha sido asignado anteriormente
			my_plantilla=Plantilla(seleccion='SELECCIONADO', usuario=my_user.first() ,jugador=delantero_random)
			my_plantilla.save()

	lista_jugadores = Jugador.objects.all()
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
	
	usuario = Usuario.objects.filter(username=username)
	nombre_liga = Liga.objects.filter(usuario__in = usuario).first().nombre

	clasif_usuarios = Usuario.objects.all().order_by("-puntuacion")		#todos los usuarios del sistema
	mis_compis = Liga.objects.filter(nombre = nombre_liga)
	
	mejores_mi_liga = []
	for i in clasif_usuarios:
		for j in mis_compis:
			if i == j.usuario:
				mejores_mi_liga.append(i)
	
	return render(request, "clasificacion.html",{'username':username,'nombre_liga':nombre_liga,'mejores_mi_liga':mejores_mi_liga})

def miEquipo(request):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.get(username=username)
	mensaje_de_error = False
	mensaje_de_errorPortero = False
	mensaje_de_errorDefensa = False
	mensaje_de_errorCentro = False
	mensaje_de_errorDelantero = False
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
					todos_jug = Plantilla.objects.filter(usuario = my_user,seleccion='SELECCIONADO')
					misma_posicion = 0
					if this_jugador.posicion == 'PORTERO':
						for j in todos_jug:
							if j.jugador.posicion == 'PORTERO':
								misma_posicion = misma_posicion + 1
								if misma_posicion >= 1:
									mensaje_de_errorPortero = True
					if this_jugador.posicion == 'DEFENSA':
							for j in todos_jug:
								if j.jugador.posicion == 'DEFENSA':
									misma_posicion = misma_posicion + 1
									if misma_posicion >= 4:
										mensaje_de_errorDefensa = True

					if this_jugador.posicion == 'CENTROCAMPISTA':
						for j in todos_jug:
							if j.jugador.posicion == 'CENTROCAMPISTA':
								misma_posicion = misma_posicion + 1
								if misma_posicion >= 4:
									mensaje_de_errorCentro = True

					if this_jugador.posicion == 'DELANTERO':
						for j in todos_jug:
							if j.jugador.posicion == 'DELANTERO':
								misma_posicion = misma_posicion + 1
								if misma_posicion >= 2:
									mensaje_de_errorDelantero = True
				
					if mensaje_de_errorPortero==False and mensaje_de_errorDefensa==False and mensaje_de_errorCentro==False and mensaje_de_errorDelantero == False:
						jug_plantilla.seleccion = 'SELECCIONADO'
						jug_plantilla.save()

		desactivar_botones = Opciones.objects.filter(botones_activos = 'NO')
		desactivacion = False
		if desactivar_botones:
			desactivacion = True

		my_plantilla_no_seleccionada = Plantilla.objects.filter(usuario=my_user, seleccion='NO SELECCIONADO')
		total_no_selec = len(Plantilla.objects.filter(usuario=my_user, seleccion='NO SELECCIONADO'))
		my_plantilla_seleccionada = Plantilla.objects.filter(usuario=my_user, seleccion='SELECCIONADO')
		total_selec = len(Plantilla.objects.filter(usuario=my_user, seleccion='SELECCIONADO'))

		ultima_jornada = Opciones.objects.get(id=1).ultima_jornada
		jugadores_de_la_jorn = Jornada.objects.filter(numero_jornada=ultima_jornada)		#filas de la jorn que este en la variable global

		return render(request, "mi_equipo.html",{'my_user':my_user,'username':username, 'my_plantilla_no_seleccionada':my_plantilla_no_seleccionada, 'my_plantilla_seleccionada':my_plantilla_seleccionada,
																'mensaje_de_error':mensaje_de_error,'total_no_selec':total_no_selec,'total_selec':total_selec, 'jugadores_de_la_jorn':jugadores_de_la_jorn,
																'desactivacion':desactivacion, 'mensaje_de_errorPortero':mensaje_de_errorPortero, 'mensaje_de_errorDefensa':mensaje_de_errorDefensa,'mensaje_de_errorCentro':mensaje_de_errorCentro,'mensaje_de_errorDelantero':mensaje_de_errorDelantero})
	else:
		return HttpResponseRedirect('/inicioSesion')


def puntuacionUsuarioJornada(request):
	numero_jorn = Opciones.objects.get(id=1).ultima_jornada
	jornada_a_sumar = Jornada.objects.filter(numero_jornada = numero_jorn, jornada_sumada = 'NO')
	if jornada_a_sumar:			#si todas las filas de la clase jornada han sido sumadas ya, esta función no hace nada
		usuarios_app = Usuario.objects.all()
		for i in usuarios_app:
			if i.presupuesto >= 0:
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
	obj_mercado = Mercado.objects.all()		#guardamos en una variable todos los objetos que hay en el mercado
	ahora = timezone.now()					#nos devuelve la hora actual
	for i in obj_mercado:
		caducidadDelJug = i.fecha_ingreso + datetime.timedelta(days=2)	#Calculamos cuando debe salir sumandole dos dias a la fecha de ingreso
		#Si la fecha actual es posterior a la de "caducidad" del jugador en el mercado entramos en el if
		if ahora > caducidadDelJug:											
			jugadorOutMercado = Mercado.objects.get(nombre_liga=i.nombre_liga,jugador=i.jugador)	#el jug que debe salir
			
			#A PARTIR DE AQUÍ SE EMPIEZA A RESOLVER LAS PUJAS
			my_jugador = jugadorOutMercado.jugador
			existe_puja = Puja.objects.filter(jugador=my_jugador)		#Comprobamos que al menos haya una puja realizada por el jugador 
			#si nadie ha pujado por el jug solo lo eliminamos del mercado, no entramos en el if
			if existe_puja:			
				#ya sabemos que al menos una puja hay, cogemos la mayor en caso de haber varias
				puja_superior = Puja.objects.filter(jugador=my_jugador).order_by("-cantidad")[0]
				#busco los usuarios de la misma liga que el jugador que queremos eliminar del mercado	
				lineas_clase_liga = Liga.objects.filter(nombre=i.nombre_liga)		
				
				for j in lineas_clase_liga:				#recorremos todos los usuarios para ver cual tiene como jugador el que acabamos de vender
					quitar_de_plantilla = Plantilla.objects.filter(usuario = j.usuario, jugador = my_jugador)
					if quitar_de_plantilla:
						quitar_de_plantilla.delete()
						j.usuario.presupuesto = j.usuario.presupuesto + puja_superior.cantidad			#sumar el dinero de la venta del jugador
						j.usuario.save()


				pujador_win = puja_superior.pujador
				#Quitarle el dinero que le ha costado el jugador de su presupuesto
				pujador_win.presupuesto = pujador_win.presupuesto - puja_superior.cantidad
				pujador_win.save()
				#asignamos el jugador a su nuevo usuario
				añadir_a_plantilla= Plantilla(seleccion='NO SELECCIONADO', usuario=pujador_win ,jugador=my_jugador)
				añadir_a_plantilla.save()	

			usuarios_pujantes = Liga.objects.filter(nombre = i.nombre_liga)
			for x in usuarios_pujantes:					#cada x una fila de la liga del jug que se va a eliminar
				puja_por_jug = Puja.objects.filter(pujador = x.usuario, jugador = my_jugador)
				puja_por_jug.delete()
			
			jugadorOutMercado.delete()		#cuando se resuelve la puja, el jugador es eliminado del mercado




def mercado(request):
	username = request.session.get("user_logeado")
	nombre_liga = Liga.objects.filter(usuario=username).first().nombre			#nombre de la liga del usuario								
	if username:																#solo entramos a la vista mercado si hay un usuario logueado
		#función que comprueba si el jugador excede el tiempo que debe estar en el mercado
		fuera_del_mercado(username)												
		#Llamamos a una función que comprueba si hay un mínimo de jug en el mercado y añade más si hay menos del mínimo 
		JugadorAñadidoPorSistema(username)
		my_user = Usuario.objects.get(username=username)						#objeto usuario con nombre username

		jugadores_en_el_mercado = Mercado.objects.filter(nombre_liga=nombre_liga)			
		mensaje_de_error = False												#inicialización de msg1
		mensaje_de_error_2 = False												#inicialización de msg2
		if request.method=="POST":
			if request.POST.get('puja'):										
				puja = request.POST.get('puja')									#puja = cantidad pujada
				id_jugador = request.POST.get('idJugador')
				jugador = Jugador.objects.get(id=id_jugador)					#objeto jugador

				#compruebo que el usuario no puja por jugador que ya es suyo
				if len(Plantilla.objects.filter(usuario=username, jugador=jugador))==0:			
					if my_user.presupuesto >= int(puja):
						#compruebo que el usuario no repite la puja
						puja_repe = Puja.objects.filter(pujador=my_user,jugador=jugador,cantidad=puja)		
						if len(puja_repe) == 0:
							la_liga = Liga.objects.filter(usuario=username)		#objeto liga del usuario
							obj = Puja(pujador=my_user, jugador=jugador,cantidad=puja,liga=la_liga.first())		#se crea la puja
							obj.save()
							
					else:
						mensaje_de_error_2 = True

				else:
					mensaje_de_error = True
		
		#Vamos a obtener la puja más alta de cada jugador en el mercado
		pujas = []
		for jug in jugadores_en_el_mercado:
			if Puja.objects.filter(jugador=jug.jugador):
				pujas_aux = Puja.objects.filter(jugador=jug.jugador).order_by("-cantidad")[0]
				pujas.append(pujas_aux)
		
		
		return render(request, "mercado.html", {'username':username,'jugadores_en_el_mercado':jugadores_en_el_mercado,'nombre_liga':nombre_liga,
													'pujas':pujas,'mensaje_de_error':mensaje_de_error,"mensaje_de_error_2":mensaje_de_error_2})
	else:
		return HttpResponseRedirect('/inicioSesion')

 
def JugadorAñadidoPorSistema(username):
	liga = Liga.objects.filter(usuario=username).first().nombre			#nombre de la liga del usuario
	minimo_jugadores = Opciones.objects.get(id=1).min_jugadores_mercado #el mínimo de jug está en opciones
	lista_jugadores = Jugador.objects.all() 	#todos los jugadores del sistema
	
	compis_liga = []							#inicialización lista de usuarios de la misma liga
	aux = Liga.objects.filter(nombre=liga)
	for i in aux:
		compis_liga.append(i.usuario)			#se añaden los usuarios a la lista

	
	while len(Mercado.objects.filter(nombre_liga = liga)) < minimo_jugadores:	#mientras no se alcance el mínimo
		jugador_random = lista_jugadores[randint(0,len(lista_jugadores)-1)]		#Obtiene un jugador al azar
		jugadores_de_compis = []		#inicializamos una lista para guardar los jug de otros compañeros de liga
		jugador_no_existe = True
		for j in compis_liga:
			filas_de_plantilla = Plantilla.objects.filter(usuario=j)	
			for m in filas_de_plantilla:
				jugadores_de_compis.append(m.jugador)		#todos los jugadores ya en la liga

		for n in jugadores_de_compis:		#recorro todos los jug de los compañeros de liga
			if n == jugador_random:			#si coincide con el jug random
				jugador_no_existe = False	#la variable se pone falso

		if jugador_no_existe:			#si la variable es true entra dentro del if
			obj = Mercado(nombre_liga=liga,jugador=jugador_random,fecha_ingreso=datetime.datetime.utcnow())
			obj.save()		#se guarda el nuevo jugador en el mercado de la liga en cuestión

 


def jugadorAlMercado(request,id):
	username = request.session.get("user_logeado")		#nombre del usuario logueado
	my_user = Usuario.objects.filter(username=username)	#objeto usuario
	my_liga = Liga.objects.filter(usuario__in=my_user)	#objeto liga a la que pertenece el usuario logueado
	#print(my_liga)
	if username:										#Si el usuario está logueado accede a la vista
		jugadorAñadido=False							#variable para mostrar text en la plantilla de jugador añadido al mercado
		mi_jugador = Jugador.objects.get(id=id)			#objeto jugador que coincide con con el id pasado por la url
		
		#busco en el mercado si ya existe el jugador
		jugadorRepetido = Mercado.objects.filter(nombre_liga=my_liga.first().nombre,jugador=mi_jugador)
	
		mensaje_de_error = False						#se inicializa el mensaje de error a falso
		if request.method=="POST":						
			if (len(jugadorRepetido) == 0):				#si el jugador no está ya en el mercado entramos al if
				obj = Mercado(nombre_liga=my_liga.first().nombre,jugador=mi_jugador,fecha_ingreso=datetime.datetime.utcnow())
				obj.save()								#guardamos el el objeto mercado que acabamos de crear
				jugadorAñadido=True						
			else:										#El jugador ya está en el mercado
				mensaje_de_error= True					#se pone a verdadero el mensaje de error
			return render(request, "jugador_al_mercado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorAñadido':jugadorAñadido,
																	'mensaje_de_error':mensaje_de_error})
		return render(request, "jugador_al_mercado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorAñadido':jugadorAñadido})
	else:
		return HttpResponseRedirect('/inicioSesion')	#si el usuario no está logueado se le redirige al inicio de sesión

	
def infoJugador(request,id):				#Vista cuando pulsamos en el nombre de un jugador
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.filter(username=username)
	if username:
		mi_jugador = Jugador.objects.get(id=id)
		
		propietario = Plantilla.objects.filter(jugador=mi_jugador).first()
		if propietario:
			propietario = propietario.usuario
		
		ult_jornada = Opciones.objects.get(id=1).ultima_jornada
		ptos_jorn = Jornada.objects.filter(jugador=mi_jugador, numero_jornada=ult_jornada).first().puntos

		return render(request, "info_jugador.html", {'username':username,'mi_jugador':mi_jugador,'propietario':propietario,"ptos_jorn":ptos_jorn})
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

def lista_jugadores_añadir(request):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.get(username=username)
	if username:
		my_plantilla = Plantilla.objects.filter(usuario=my_user)
		#print(my_plantilla)
		return render(request, "lista_jugadores_añadir.html", {'username':username,'my_user':my_user, 'my_plantilla':my_plantilla})
	else:
		return HttpResponseRedirect('/inicioSesion')

def lista_jugadores_eliminar(request):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.get(username=username)
	if username:
		my_plantilla = Plantilla.objects.filter(usuario=my_user)
		#print(my_plantilla)
		return render(request, "lista_jugadores_eliminar.html", {'username':username,'my_user':my_user, 'my_plantilla':my_plantilla})
	else:
		return HttpResponseRedirect('/inicioSesion')

def eliminarJugador(request,id):
	username = request.session.get("user_logeado")		#nombre del usuario logueado
	#my_user = Usuario.objects.filter(username=username)	#objeto usuario	

	if username:										#Si el usuario está logueado accede a la vista
		jugadorEliminado=False							#variable para mostrar text en la plantilla de jugador eliminado del equipo
		mi_jugador = Jugador.objects.get(id=id)			#objeto jugador que coincide con con el id pasado por la url
		
		if request.method=="POST":
			obj = Plantilla.objects.get(jugador=mi_jugador)
			obj.delete()
			jugadorEliminado=True

		return render(request, "jugador_eliminado.html",{'username':username,'mi_jugador':mi_jugador,'jugadorEliminado':jugadorEliminado})
	else:
		return HttpResponseRedirect('/inicioSesion')	#si el usuario no está logueado se le redirige al inicio de sesión


def ranking(request):
	username = request.session.get("user_logeado")
	my_user = Usuario.objects.filter(username=username).first()
	my_plantilla_seleccionada = Plantilla.objects.filter(usuario=my_user, seleccion='SELECCIONADO')

	ultima_jornada = Opciones.objects.get(id=1).ultima_jornada
	jugadores_de_la_jorn = Jornada.objects.filter(numero_jornada=ultima_jornada)
	


	return render(request, "ranking.html", locals())
	



