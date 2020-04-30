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
	puntuacion=models.IntegerField()

	def __str__(self):
		return '%s %s, %s' % (self.nombre, self.apellidos, self.equipo) 	

class Liga(models.Model):
	nombre=models.CharField(max_length=40)
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

	def __str__(self):
		return 'Liga %s' % (self.nombre)

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

class Mercado(models.Model):
	liga_mercado = models.ForeignKey(Liga, on_delete=models.CASCADE)
	jugador_mercado = models.ForeignKey(Jugador, on_delete=models.CASCADE)

	def __str__(self):
		return 'Jugador %s de la liga %s' % (self.jugador_mercado, self.liga_mercado)
		