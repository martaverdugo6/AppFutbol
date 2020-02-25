from django.contrib import admin
from gestionApp.models import usuario

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
	list_display=("nombre","apellidos","email","nick")
	search_fields=("apellidos", "email","nick")
		



admin.site.register(usuario, UsuarioAdmin)
