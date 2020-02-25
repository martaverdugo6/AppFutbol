from django import forms

from gestionApp.models import usuario

class form_user(forms.ModelForm):

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
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellidos': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'nick': forms.TextInput(attrs={'class':'form-control'}),
			'password': forms.TextInput(attrs={'class':'form-control'}),
		}
