from django.contrib import admin
from gestionApp.models import usuario, jugador, liga

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
	list_display=("nombre","apellidos","email","mi_equipo")
	search_fields=("apellidos", "email","mi_equipo")
		
class JugadorAdmin(admin.ModelAdmin):
	list_display=("nombre", "apellidos","equipo","posicion")
	search_fields=("nombre", "apellidos","equipo")

class LigaAdmin(admin.ModelAdmin):
	list_display=("nombre",)
	search_fields=("nombre",)


admin.site.register(usuario, UsuarioAdmin)
admin.site.register(jugador, JugadorAdmin)
admin.site.register(liga, LigaAdmin)