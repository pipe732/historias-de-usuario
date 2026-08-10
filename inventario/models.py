from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True, verbose_name="Código / SKU")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock / Cantidad")

    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
        verbose_name="Categoría"
    )

    estante = models.ForeignKey(
        'almacenamiento.Estante',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
        verbose_name="Estante"
    )

    numero_serie = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número de serie")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para préstamo")
    ubicacion = models.CharField(max_length=150, blank=True, null=True, verbose_name="Almacén / Estante")
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

class Proveedor(models.Model):
    nit_proveedor = models.CharField(max_length=50, unique=True, verbose_name="NIT")
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de contacto")
    correo_proveedor = models.EmailField(verbose_name="Correo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nit_proveedor"]

    def __str__(self):
        return self.nit_proveedor


class Inventario(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="inventarios",
        verbose_name="Producto"
    )
    id_estante = models.CharField(max_length=100, verbose_name="Estante")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad")
    responsable = models.CharField(max_length=150, verbose_name="Responsable")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        ordering = ["id_estante"]
        indexes = [models.Index(fields=['id_estante'])]

    def __str__(self):
        return f"Inventario #{self.id} - {self.producto.nombre}"


class Movimientos(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
        ("ajuste", "Ajuste"),
    ]

    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name="movimientos", verbose_name="Inventario")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos", verbose_name="Proveedor")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    tipo_de_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES, verbose_name="Tipo de movimiento")
    fecha_movimiento = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de movimiento")

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ["-fecha_movimiento"]
        indexes = [
            models.Index(fields=['fecha_movimiento']),
            models.Index(fields=['tipo_de_movimiento']),
        ]

    def __str__(self):
        return f"Movimiento #{self.id} - {self.tipo_de_movimiento}"


class Detalle_Movimientos(models.Model):
    movimiento = models.ForeignKey(Movimientos, on_delete=models.CASCADE, related_name="detalles", verbose_name="Movimiento")
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name="detalles", verbose_name="Inventario")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Detalle de movimiento"
        verbose_name_plural = "Detalles de movimiento"

    def __str__(self):
        return f"Detalle #{self.id} de Movimiento #{self.movimiento_id}"
    
class Edicion_limitada(models.Model):
    ESTADO = [
        ('V', 'Vigente'),
        ('D', 'Descontinuado'),
    ]
    producto = models.OneToOneField(Producto,on_delete=models.CASCADE,)      
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20,choices=ESTADO)
    observaciones = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateTimeField()


    def __str__(self):
        return f"{self.producto.codigo_sku}  {self.nombre}  {self.estado}"


class MovimientoKardex(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada (Stock)'),
        ('salida', 'Salida (Baja)'),
        ('prestamo', 'Préstamo Entregado'),
        ('devolucion', 'Devolución Recibida'),
        ('ajuste', 'Ajuste Manual'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="kardex_movimientos", verbose_name="Producto")
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    stock_anterior = models.PositiveIntegerField(default=0, verbose_name="Stock anterior")
    stock_nuevo = models.PositiveIntegerField(default=0, verbose_name="Stock nuevo")
    usuario_nombre = models.CharField(max_length=150, blank=True, default="Sistema", verbose_name="Usuario / Responsable")
    observaciones = models.TextField(blank=True, default="", verbose_name="Observaciones")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Movimiento Kardex"
        verbose_name_plural = "Movimientos Kardex"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"[{self.tipo_movimiento.upper()}] {self.producto.nombre} ({self.cantidad}) - {self.creado_en.strftime('%d/%m/%Y %H:%M')}"
    