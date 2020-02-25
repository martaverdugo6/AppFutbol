from django.db import models

# Create your models here.

class usuario(models.Model):
	nombre=models.CharField(max_length=30)
	apellidos=models.CharField(max_length=80)
	email=models.EmailField()
	nick=models.CharField(max_length=30)
	password=models.CharField(max_length=50)
	puntuacion=models.IntegerField()
	presupuesto=models.IntegerField()

	def __str__(self):
		return self.nombre 
