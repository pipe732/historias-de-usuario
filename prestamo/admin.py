from django.contrib import admin
from .models import Prestamo, DetallePrestamo


class DetallePrestamoInline(admin.TabularInline):
    model = DetallePrestamo
    extra = 0


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('codigo_prestamo', 'documento', 'estado', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('documento__documento', 'observaciones')
    ordering = ('-fecha',)
    inlines = [DetallePrestamoInline]


@admin.register(DetallePrestamo)
class DetallePrestamoAdmin(admin.ModelAdmin):
    list_display = ('numero_detalle', 'codigo_prestamo', 'codigo_herramienta', 'cantidad')
    search_fields = ('codigo_prestamo__documento__documento', 'codigo_herramienta__nombre_herramienta')