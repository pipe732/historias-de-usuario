from django.contrib import admin
from .models import Proveedor

# Register your models here.
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nit_proveedor", "telefono_contacto", "correo_proveedor", "descripcion")
    search_fields = ("nit_proveedor", "telefono_contacto", "correo_proveedor", "descripcion")
    ordering = ("nit_proveedor",)
