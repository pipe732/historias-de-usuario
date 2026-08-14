from django.contrib import admin
from .models import DevolucionHerramienta


@admin.register(DevolucionHerramienta)
class DevolucionHerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo_devolucion', 'codigo_prestamo', 'codigo_recibe', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('codigo_prestamo__documento__documento', 'observaciones')
    ordering = ('-fecha',)