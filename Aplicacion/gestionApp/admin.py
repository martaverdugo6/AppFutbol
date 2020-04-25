from django.contrib import admin

# Register your models here.
from django.contrib import admin
from gestionApp.models import Usuario, Jugador, Plantilla, Liga, Mercado

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
	list_display=("username","email","mi_equipo")
	search_fields=("username", "email","mi_equipo")
		
class JugadorAdmin(admin.ModelAdmin):
	list_display=("nombre", "apellidos","equipo","posicion")
	search_fields=("nombre", "apellidos","equipo")

class LigaAdmin(admin.ModelAdmin):
	list_display=("nombre","usuario")
	search_fields=("nombre","usuario")

class PlantillaAdmin(admin.ModelAdmin):
	list_display=("usuario",)
	search_fields=("usuario",)

class MercadoAdmin(admin.ModelAdmin):
	list_display=("liga",)
	search_fields=("liga",)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Plantilla, PlantillaAdmin)
admin.site.register(Liga, LigaAdmin)
admin.site.register(Mercado, MercadoAdmin)