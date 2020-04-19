from django import forms

from gestionApp.models import usuario ,liga

class form_alta_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario, mismo nombre que en models
		fields =[
			'nombre',
			'email',
			'mi_equipo',
			'password',	
		]
		labels = {
			'nombre': 'Nombre de usuario',
			'email': 'Email',
			'mi_equipo': 'Nombre de equipo',
			'password': 'Contraseña',
		}



class form_login_usuario(forms.Form):

	nombre_de_usuario = forms.CharField()
	contraseña = forms.CharField(widget=forms.PasswordInput())

class form_contact(forms.Form):

	asunto=forms.CharField()
	email=forms.CharField()
	mensaje=forms.CharField()


class form_liga(forms.ModelForm):

	class Meta:
		model = liga

		fields=[
			'nombre',

		]
		labels={
			'nombre':'Nombre de la liga',
		}
