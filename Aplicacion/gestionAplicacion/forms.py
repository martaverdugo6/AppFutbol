from django import forms

from gestionAplicacion.models import usuario ,liga

class form_alta_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario, mismo nombre que en models
		fields =[
			'username',
			'email',
			'mi_equipo',
			'password',	
		]
		labels = {
			'username': 'Nombre de usuario',
			'email': 'Email',
			'mi_equipo': 'Nombre de equipo',
			'password': 'Contraseña',
		}



class form_login_usuario(forms.ModelForm):

	class Meta:
		model = usuario

		#Campos que quiero que aparezcan en el formulario, mismo nombre que en models
		fields =[
			'username',
			'password',	
		]
		labels = {
			'username': 'Nombre de usuario',
			'password': 'Contraseña',
		}

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
