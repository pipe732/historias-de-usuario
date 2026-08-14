from django.db import models
from almacenamiento.models import Existencia


class CategoriaHerramienta(models.Model):
    codigo_categoria = models.AutoField(primary_key=True, db_column='codigo_categoria')
    tipo_herramienta = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de herramienta")
    nombre_categoria = models.CharField(max_length=100, verbose_name="Nombre de categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        db_table = 'categoria_herramienta'
        verbose_name = "Categoría de Herramienta"
        verbose_name_plural = "Categorías de Herramientas"
        ordering = ["nombre_categoria"]

    @property
    def nombre(self):
        return self.nombre_categoria

    @nombre.setter
    def nombre(self, val):
        self.nombre_categoria = val

    def __str__(self):
        return self.nombre_categoria


# Alias para retrocompatibilidad
Categoria = CategoriaHerramienta


class Herramienta(models.Model):
    codigo_herramienta = models.AutoField(primary_key=True, db_column='codigo_herramienta')
    codigo_SKU = models.CharField(max_length=50, unique=True, blank=True, null=True, db_column='codigo_SKU', verbose_name="Código SKU")
    nombre_herramienta = models.CharField(max_length=100, db_column='nombre_herramienta', verbose_name="Nombre de herramienta")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    disponibilidad = models.CharField(max_length=50, blank=True, null=True, verbose_name="Disponibilidad")
    fecha_ingreso = models.DateField(blank=True, null=True, verbose_name="Fecha de ingreso")
    codigo_categoria = models.ForeignKey(
        CategoriaHerramienta,
        on_delete=models.RESTRICT,
        db_column='codigo_categoria',
        related_name='herramientas',
        verbose_name="Categoría"
    )

    class Meta:
        db_table = 'herramienta'
        verbose_name = "Herramienta"
        verbose_name_plural = "Herramientas"
        ordering = ["nombre_herramienta"]

    # Propiedades de compatibilidad con Producto
    @property
    def codigo_sku(self):
        return self.codigo_SKU

    @codigo_sku.setter
    def codigo_sku(self, val):
        self.codigo_SKU = val

    @property
    def nombre(self):
        return self.nombre_herramienta

    @nombre.setter
    def nombre(self, val):
        self.nombre_herramienta = val

    @property
    def categoria(self):
        return self.codigo_categoria

    @categoria.setter
    def categoria(self, val):
        self.codigo_categoria = val

    @property
    def disponible(self):
        return self.disponibilidad == 'Disponible' if self.disponibilidad else True

    @disponible.setter
    def disponible(self, val):
        self.disponibilidad = 'Disponible' if val else 'No disponible'

    def __str__(self):
        sku = f"[{self.codigo_SKU}] " if self.codigo_SKU else ""
        return f"{sku}{self.nombre_herramienta}"


# Alias para retrocompatibilidad con Producto
Producto = Herramienta


class Proveedor(models.Model):
    codigo_proveedor = models.AutoField(primary_key=True, db_column='codigo_proveedor')
    nit_proveedor = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="NIT")
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono de contacto")
    correo_proveedor = models.CharField(max_length=100, blank=True, null=True, verbose_name="Correo del proveedor")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        db_table = 'proveedor'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nit_proveedor"]

    def __str__(self):
        return self.nit_proveedor or f"Proveedor #{self.codigo_proveedor}"


class Suministro(models.Model):
    codigo_suministro = models.AutoField(primary_key=True, db_column='codigo_suministro')
    codigo_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.RESTRICT,
        db_column='codigo_proveedor',
        related_name='suministros',
        verbose_name="Proveedor"
    )
    codigo_herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.RESTRICT,
        db_column='codigo_herramienta',
        related_name='suministros',
        verbose_name="Herramienta"
    )
    codigo_inventario = models.ForeignKey(
        Existencia,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column='codigo_inventario',
        related_name='suministros',
        verbose_name="Existencia"
    )
    fecha = models.DateField(verbose_name="Fecha")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        db_table = 'suministro'
        verbose_name = "Suministro"
        verbose_name_plural = "Suministros"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Suministro #{self.codigo_suministro} - {self.codigo_herramienta.nombre_herramienta} ({self.cantidad})"


class Traslado(models.Model):
    codigo_traslado = models.AutoField(primary_key=True, db_column='codigo_traslado')
    cantidad_total = models.IntegerField(verbose_name="Cantidad Total")
    tipo_movimiento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tipo de movimiento")
    fecha_movimiento = models.DateField(verbose_name="Fecha de movimiento")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    codigo_inventario = models.ForeignKey(
        Existencia,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column='codigo_inventario',
        related_name='traslados',
        verbose_name="Existencia"
    )

    class Meta:
        db_table = 'traslado'
        verbose_name = "Traslado"
        verbose_name_plural = "Traslados"
        ordering = ["-fecha_movimiento"]

    def __str__(self):
        return f"Traslado #{self.codigo_traslado} - {self.fecha_movimiento}"


class DetalleTraslado(models.Model):
    codigo_detalle = models.AutoField(primary_key=True, db_column='codigo_detalle')
    codigo_traslado = models.ForeignKey(
        Traslado,
        on_delete=models.CASCADE,
        db_column='codigo_traslado',
        related_name='detalles',
        verbose_name="Traslado"
    )
    codigo_herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.RESTRICT,
        db_column='codigo_herramienta',
        related_name='detalles_traslado',
        verbose_name="Herramienta"
    )
    cantidad = models.IntegerField(verbose_name="Cantidad")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        db_table = 'detalle_traslado'
        verbose_name = "Detalle de Traslado"
        verbose_name_plural = "Detalles de Traslado"

    def __str__(self):
        return f"Detalle #{self.codigo_detalle} de Traslado #{self.codigo_traslado_id}"


# Aliases de retrocompatibilidad para vistas
Inventario = Existencia
Movimientos = Traslado
Detalle_Movimientos = DetalleTraslado
MovimientoKardex = DetalleTraslado
Edicion_limitada = Herramienta