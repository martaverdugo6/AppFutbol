from django import forms

from gestionApp.models import Usuario,Liga

class form_alta_usuario(forms.ModelForm):
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
		widgets = {
     		'password': forms.PasswordInput()
        }



class form_login_usuario(forms.ModelForm):
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
		widgets = {
     		'password': forms.PasswordInput()
        }


class form_cambio_password(forms.Form):
	Contraseña_actual=forms.CharField(widget=forms.PasswordInput)
	Nueva_contraseña=forms.CharField(widget=forms.PasswordInput)

class form_cambio_email(forms.Form):
	Email_actual=forms.EmailField()
	Nuevo_email=forms.EmailField()

class form_cambio_equipo(forms.Form):
	Nombre_actual_del_equipo=forms.CharField(max_length=30)
	Nuevo_nombre_para_el_equipo=forms.CharField(max_length=30)

class form_liga(forms.ModelForm):

	class Meta:
		model = Liga

		fields=[
			'nombre',

		]
		labels={
			'nombre':'Nombre de la liga',
		}
