from django.db import models

class Proveedor(models.Model):
    nit_proveedor = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de contacto")
    correo_proveedor = models.EmailField(verbose_name="Correo electrónico")
    descripcion = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"

    def __str__(self):
        return f"{self.nit_proveedor}"

class Trabajador(models.Model):
    nombre= models.CharField(unique=True,verbose_name="nombre")
    cedula = models.CharField(max_length=20, verbose_name="cedula de ciudadania")
    correo_trabajador = models.EmailField(verbose_name="Correo electrónico")
    fecha_nacimiento = models.CharField(max_length=20, unique=True, verbose_name="fecha de nacimiento ")

    class Meta:
        verbose_name = "trabajador"
        verbose_name_plural = "trabajadores"

    def __str__(self):
        return f"{self.nombre_trabajador}"


