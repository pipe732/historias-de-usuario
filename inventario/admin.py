from django.contrib import admin
from .models import Producto, Categoria, Proveedor, Inventario, Movimientos, Detalle_Movimientos

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Inventario)
admin.site.register(Movimientos)
admin.site.register(Detalle_Movimientos)

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "creado_en")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_sku",
        "nombre",
        "categoria",
        "stock",
        "disponible",
        "ubicacion",
        "creado_en",
        "actualizado_en",
    )
    list_filter = ("categoria", "disponible")
    search_fields = ("codigo_sku", "nombre", "descripcion", "numero_serie", "ubicacion")
    ordering = ("nombre",)
