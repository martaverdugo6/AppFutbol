from django import forms

from gestionApp.models import usuario

class form_user(forms.ModelForm):

	class Meta:
		model = usuario

		fields =[
			'nombre',
			'apellidos',
			'email',
			'nick',
			'password',
			'puntuacion',
			'presupuesto',
		]
		labels = {
			'nombre': 'Nombre',
			'apellidos': 'Apellidos',
			'email': 'Email',
			'nick': 'Nick',
			'password': 'Contraseña',
			'puntuacion': 'Puntuacion',
			'presupuesto':'Presupuesto',
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellidos': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'nick': forms.TextInput(attrs={'class':'form-control'}),
			'password': forms.TextInput(attrs={'class':'form-control'}),
			'puntuacion': forms.TextInput(attrs={'class':'form-control'}),
			'presupuesto':forms.TextInput(attrs={'class':'form-control'}),
		}
