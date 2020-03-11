from django.contrib import admin
from gestionApp.models import usuario, jugador

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
	list_display=("nombre","apellidos","email","mi_equipo")
	search_fields=("apellidos", "email","mi_equipo")
		
class JugadorAdmin(admin.ModelAdmin):
	list_display=("nombre", "apellidos","equipo","posicion")
	search_fields=("nombre", "apellidos","equipo")

admin.site.register(usuario, UsuarioAdmin)
admin.site.register(jugador, JugadorAdmin)