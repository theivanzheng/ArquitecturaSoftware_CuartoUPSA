from django.contrib import admin
from .models import Cliente, Coche, Servicio, CocheServicio


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'email')


@admin.register(Coche)
class CocheAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'marca', 'modelo', 'anio', 'cliente')
    list_filter = ('marca',)
    search_fields = ('matricula', 'marca', 'modelo')


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'precio', 'fecha')
    list_filter = ('fecha',)


@admin.register(CocheServicio)
class CocheServicioAdmin(admin.ModelAdmin):
    list_display = ('coche', 'servicio', 'observaciones')
