from django.contrib import admin
from .models import Producto, Categoria, Proveedor, Inventario, Movimientos, Detalle_Movimientos

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Inventario)
admin.site.register(Movimientos)
admin.site.register(Detalle_Movimientos)

# Register your models here.
