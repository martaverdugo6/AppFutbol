from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from gestionApp.models import Usuario, Jugador, Plantilla, Liga, Mercado, Puja, Jornada, Opciones

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
	list_display=("usuario","jugador","seleccion")
	search_fields=("usuario",)

class MercadoAdmin(admin.ModelAdmin):
	list_display=("nombre_liga","jugador","fecha_ingreso")  
	search_fields=("nombre_liga","jugador","fecha_ingreso")  

class PujaAdmin(admin.ModelAdmin):
	list_display=("pujador","jugador","cantidad","liga") 
	search_fields=("pujador","jugador")

class JornadaAdmin(admin.ModelAdmin):
	list_display=("numero_jornada","jugador","puntos","jornada_sumada")
	search_fields=("numero_jornada",)

class OpcionesAdmin(admin.ModelAdmin):
	list_display=("presupuesto_de_inicio","max_num_usuarios_liga","num_jug_plant_inicio","ultima_jornada","sumar_puntos_jorn", "botones_activos","min_jugadores_mercado")
	search_fields=("presupuesto_de_inicio","max_num_usuarios_liga","num_jug_plant_inicio","ultima_jornada","sumar_puntos_jorn", "botones_activos", "min_jugadores_mercado")

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Plantilla, PlantillaAdmin)
admin.site.register(Liga, LigaAdmin)
admin.site.register(Mercado, MercadoAdmin)
admin.site.register(Puja, PujaAdmin)
admin.site.register(Jornada, JornadaAdmin)
admin.site.register(Opciones, OpcionesAdmin)