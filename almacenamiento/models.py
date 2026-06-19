from django.db import models
from almacenamiento.models import Estante

class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True, verbose_name="Código / SKU")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock / Cantidad")

    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="productos", verbose_name="Categoría"
    )

    numero_serie = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número de serie")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para préstamo")

    # ── NUEVO: relación real con Estante en vez de texto libre ──
    estante = models.ForeignKey(
        Estante, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="productos", verbose_name="Estante"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=['codigo_sku']),
            models.Index(fields=['nombre']),
            models.Index(fields=['stock']),
        ]

    def __str__(self):
        return f"[{self.codigo_sku}] {self.nombre}"


class Almacen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # ← unique
    detalles = models.TextField(blank=True, null=True)
    capacidad = models.PositiveIntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Estante(models.Model):
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)  # ← unique
    detalles = models.TextField(blank=True, null=True)
    capacidad = models.PositiveIntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo