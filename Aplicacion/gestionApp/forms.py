from django import forms

from gestionApp.models import usuario

class form_alta_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario, mismo nombre que en models
		fields =[
			'nombre',
			'apellidos',
			'email',
			'mi_equipo',
			'password',	
		]
		labels = {
			'nombre': 'Nombre',
			'apellidos': 'Apellidos',
			'email': 'Email',
			'mi_equipo': 'Nombre de equipo',
			'password': 'Contraseña',
		}



class form_login_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario
		fields =[
			'mi_equipo',
			'password',	
		]
		
		labels = {
			'mi_equipo': 'Nombre de equipo',
			'password': 'Contraseña',
		}
