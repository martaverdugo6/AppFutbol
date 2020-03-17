from django.db import models

# Create your models here.

class usuario(models.Model):
	nombre=models.CharField(max_length=30)
	apellidos=models.CharField(max_length=80)
	email=models.EmailField()
	mi_equipo=models.CharField(max_length=30)
	password=models.CharField(max_length=50)
	puntuacion=models.IntegerField()
	presupuesto=models.IntegerField()

	def __str__(self):
		return self.email 

class jugador(models.Model):
	PORTERO='PORTERO'
	DEFENSA='DEFENSA'
	MEDIOCENTRO='MEDIOCENTRO'
	DELANTERO='DELANTERO'
	ELECCION_POSICION=(
		
		(PORTERO, u'Portero'),
		(DEFENSA, u'Defensa'),
		(MEDIOCENTRO, u'Mediocentro'),
		(DELANTERO, u'Delantero'),

	)

	nombre=models.CharField(max_length=30)
	apellidos=models.CharField(max_length=80)
	equipo=models.CharField(max_length=80)
	valor_mercado=models.IntegerField()
	posicion=models.CharField(max_length=30, choices=ELECCION_POSICION)
	puntuacion=models.IntegerField()

	def __str__(self):
		return '%s %s %s' % (self.nombre, self.apellidos, self.equipo) 	

class liga(models.Model):
	nombre=models.CharField(max_length=40)
	usuarios = models.ForeignKey(usuario, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre