from django.db import models

class Proveedor(models.Model):
    nit_proveedor = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de contacto")
    correo_proveedor = models.EmailField(verbose_name="Correo electrónico")
    descripcion = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.nit_proveedor}"