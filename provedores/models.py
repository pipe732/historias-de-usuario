from django.db import models


class Proveedor(models.Model):
    codigo_proveedor = models.AutoField(primary_key=True, db_column='codigo_proveedor')
    nit_proveedor = models.CharField(max_length=50, unique=True, verbose_name="NIT")
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de contacto")
    correo_proveedor = models.EmailField(max_length=100, verbose_name="Correo electrónico")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        db_table = "proveedor"
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"

    def __str__(self):
        return f"{self.nit_proveedor}"


class Trabajador(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    cedula = models.CharField(max_length=20, verbose_name="Cédula de ciudadanía")
    correo_trabajador = models.EmailField(verbose_name="Correo electrónico")
    fecha_nacimiento = models.CharField(max_length=20, verbose_name="Fecha de nacimiento")

    class Meta:
        verbose_name = "trabajador"
        verbose_name_plural = "trabajadores"

    def __str__(self):
        return f"{self.nombre}"
