from django import forms

from gestionApp.models import Usuario,Liga

class form_alta_usuario(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Usuario

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
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Usuario

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

class form_cambio_password(forms.Form):
	Contraseña_actual=forms.CharField()
	Nueva_contraseña=forms.CharField()

class form_liga(forms.ModelForm):

	class Meta:
		model = Liga

		fields=[
			'nombre',

		]
		labels={
			'nombre':'Nombre de la liga',
		}
