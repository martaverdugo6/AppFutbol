from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Usuario(models.Model):
	username=models.CharField(max_length=50, primary_key=True) 
	email=models.EmailField()
	mi_equipo=models.CharField(max_length=30)
	password=models.CharField(max_length=50)
	puntuacion=models.IntegerField()
	presupuesto=models.IntegerField()

	def __str__(self):
		return self.username 

class Jugador(models.Model):
	PORTERO='PORTERO'
	DEFENSA='DEFENSA'
	MEDIOCENTRO='CENTROCAMPISTA'
	DELANTERO='DELANTERO'
	ELECCION_POSICION=(
		
		(PORTERO, u'Portero'),
		(DEFENSA, u'Defensa'),
		(MEDIOCENTRO, u'Centrocampista'),
		(DELANTERO, u'Delantero'),

	)

	nombre=models.CharField(max_length=30)
	apellidos=models.CharField(max_length=80)
	equipo=models.CharField(max_length=80)
	posicion=models.CharField(max_length=30, choices=ELECCION_POSICION)

	def __str__(self):
		return '%s %s, %s' % (self.nombre, self.apellidos, self.equipo) 	

class Plantilla(models.Model):
	SELECCIONADO='SELECCIONADO'
	NO_SELECCIONADO='NO SELECCIONADO'
	SELECCION_JUGADOR=(
		
		(SELECCIONADO, u'Seleccionado'),
		(NO_SELECCIONADO, u'No seleccionado'),

	)

	seleccion=models.CharField(max_length=30, choices=SELECCION_JUGADOR)
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)

	def __str__(self):
		return '%s tiene a %s, %s' % (self.usuario, self.jugador, self.seleccion)

class Liga(models.Model):
	nombre=models.CharField(max_length=40)
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

	def __str__(self):
		return 'Liga %s' % (self.nombre)

class Mercado(models.Model):
	liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
	jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
	fecha_ingreso = models.DateTimeField()

	def __str__(self):
		return 'Jugador %s de la liga %s' % (self.jugador_mercado, self.liga_mercado)
		
class Puja(models.Model):
	pujador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
	cantidad = models.IntegerField()
	liga = models.ForeignKey(Liga, on_delete=models.CASCADE)

	def __str__(self):
		return '%s ha pujado %s por %s' % (self.pujador, self.cantidad, self.jugador)

class Jornada(models.Model):
	SI ='SI'
	NO='NO'
	JORNADA_SUMADA=(
		
		(SI, u'SI'),
		(NO, u'No'),

	)

	jornada_sumada = models.CharField(max_length=30, choices=JORNADA_SUMADA)
	numero_jornada = models.IntegerField()
	jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
	puntos = models.IntegerField()

	def __str__(self):
		return '%s ha conseguido %s puntos en la jornada %s' % (self.jugador, self.puntos, self.numero_jornada)

class Opciones(models.Model):
	SI ='SI'
	NO='NO'
	ACTIVO_SUMAR_PUNTOS=(
		
		(SI, u'SI'),
		(NO, u'No'),

	)
	presupuesto_de_inicio = models.IntegerField()
	max_num_usuarios_liga = models.IntegerField()
	num_jug_plant_inicio = models.IntegerField()
	ultima_jornada = models.IntegerField()
	sumar_puntos_jorn = models.CharField(max_length=30, choices=ACTIVO_SUMAR_PUNTOS)