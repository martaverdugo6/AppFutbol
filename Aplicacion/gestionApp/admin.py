from django.contrib import admin
from gestionApp.models import usuario, jugador, liga, plantilla, mercado

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

class PlantillaAdmin(admin.ModelAdmin):
	list_display=("usuario",)
	search_fields=("usuario",)

class MercadoAdmin(admin.ModelAdmin):
	list_display=("liga",)
	search_fields=("liga",)

admin.site.register(usuario, UsuarioAdmin)
admin.site.register(jugador, JugadorAdmin)
admin.site.register(liga, LigaAdmin)
admin.site.register(plantilla, PlantillaAdmin)
admin.site.register(mercado, MercadoAdmin)