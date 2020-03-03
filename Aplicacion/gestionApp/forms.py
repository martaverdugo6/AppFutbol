from django import forms

from gestionApp.models import usuario

class form_alta_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario
		fields =[
			'nombre',
			'apellidos',
			'email',
			'nick',
			'password',	
		]
		labels = {
			'nombre': 'Nombre',
			'apellidos': 'Apellidos',
			'email': 'Email',
			'nick': 'Nick',
			'password': 'Contraseña',
		}



class form_login_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario
		fields =[
			'nick',
			'password',	
		]
		
		labels = {
			'nick': 'Nick',
			'password': 'Contraseña',
		}
