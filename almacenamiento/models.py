from django.db import models


class Almacen(models.Model):
    codigo_almacen = models.AutoField(primary_key=True, db_column='codigo_almacen')
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    dimensiones = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dimensiones")
    ubicacion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ubicación")

    class Meta:
        db_table = 'almacen'
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Estante(models.Model):
    num_estante = models.AutoField(primary_key=True, db_column='num_estante')
    codigo = models.CharField(max_length=50, verbose_name="Código")
    dimensiones = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dimensiones")
    codigo_almacen = models.ForeignKey(
        Almacen,
        on_delete=models.RESTRICT,
        db_column='codigo_almacen',
        related_name='estantes',
        verbose_name="Almacén"
    )

    class Meta:
        db_table = 'estante'
        verbose_name = "Estante"
        verbose_name_plural = "Estantes"
        ordering = ['codigo']

    @property
    def almacen(self):
        return self.codigo_almacen

    @almacen.setter
    def almacen(self, val):
        self.codigo_almacen = val

    def __str__(self):
        return f"{self.codigo} ({self.codigo_almacen.nombre})"


class Existencia(models.Model):
    codigo_existencias = models.AutoField(primary_key=True, db_column='codigo_existencias')
    cantidad = models.IntegerField(default=0, verbose_name="Cantidad")
    responsable = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsable")
    fecha_creacion = models.DateField(blank=True, null=True, verbose_name="Fecha de creación")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    num_estante = models.ForeignKey(
        Estante,
        on_delete=models.RESTRICT,
        db_column='num_estante',
        related_name='existencias',
        verbose_name="Estante"
    )

    class Meta:
        db_table = 'existencia'
        verbose_name = "Existencia"
        verbose_name_plural = "Existencias"
        ordering = ['-codigo_existencias']

    @property
    def estante(self):
        return self.num_estante

    @estante.setter
    def estante(self, val):
        self.num_estante = val

    def __str__(self):
        return f"Existencia #{self.codigo_existencias} - {self.cantidad} unidades"
