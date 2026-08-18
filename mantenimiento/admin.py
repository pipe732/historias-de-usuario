from django.contrib import admin
from .models import Mantenimiento, DetalleMantenimiento, BitacoraEstado


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = [
        'num_mantenimiento',
        'codigo_herramienta',
        'tipo_mantenimiento',
        'fecha_ingreso',
        'fecha_salida',
    ]
    list_filter = ['tipo_mantenimiento', 'fecha_ingreso']
    search_fields = ['codigo_herramienta__nombre_herramienta', 'observaciones']
    ordering = ['-fecha_ingreso']


@admin.register(DetalleMantenimiento)
class DetalleMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['detalle_mantenimiento', 'num_mantenimiento', 'fecha_mantenimiento']
    ordering = ['-fecha_mantenimiento']


@admin.register(BitacoraEstado)
class BitacoraEstadoAdmin(admin.ModelAdmin):
    list_display = ['codigo_bitacora', 'num_mantenimiento', 'estado', 'nivel_estado']
