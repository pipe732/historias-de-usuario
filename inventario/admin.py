from django.contrib import admin
from .models import Herramienta, CategoriaHerramienta, Proveedor, Suministro, Traslado, DetalleTraslado

admin.site.register(Herramienta)
admin.site.register(CategoriaHerramienta)
admin.site.register(Proveedor)
admin.site.register(Suministro)
admin.site.register(Traslado)
admin.site.register(DetalleTraslado)
