from django.db import models
from django.utils import timezone
from inventario.models import Herramienta

ESTADO_REGISTRO_CHOICES = [
    ("abierto", "Abierto"),
    ("en_proceso", "En proceso"),
    ("cerrado", "Cerrado"),
    ("cancelado", "Cancelado"),
]

MOTIVO_CAMBIO_CHOICES = [
    ("correccion_error", "Corrección de error"),
    ("actualizacion_imprevisto", "Actualización por imprevisto"),
    ("adicion_evidencia", "Adición de evidencia"),
    ("ajuste_estado", "Ajuste de estado"),
    ("otro", "Otro"),
]


class TipoEstado(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False


class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False


class MantenimientoCambio(models.Model):
    class Meta:
        managed = False


class Mantenimiento(models.Model):
    num_mantenimiento = models.AutoField(
        primary_key=True, db_column='num_mantenimiento'
    )
    tipo_mantenimiento = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Tipo de mantenimiento"
    )
    fecha_ingreso = models.DateField(
        default=timezone.now, verbose_name="Fecha de ingreso"
    )
    fecha_salida = models.DateField(
        blank=True, null=True, verbose_name="Fecha de salida"
    )
    observaciones = models.TextField(
        blank=True, null=True, verbose_name="Observaciones"
    )
    codigo_herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.RESTRICT,
        db_column='codigo_herramienta',
        related_name='mantenimientos',
        verbose_name="Herramienta"
    )

    class Meta:
        db_table = 'mantenimiento'
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha_ingreso"]

    @property
    def producto(self):
        return self.codigo_herramienta

    @producto.setter
    def producto(self, val):
        self.codigo_herramienta = val

    def __str__(self):
        return f"Mantenimiento #{self.num_mantenimiento} — {self.codigo_herramienta}"


class DetalleMantenimiento(models.Model):
    detalle_mantenimiento = models.AutoField(
        primary_key=True, db_column='detalle_mantenimiento'
    )
    accion_realizada = models.TextField(
        blank=True, null=True, verbose_name="Acción realizada"
    )
    materiales_usados = models.TextField(
        blank=True, null=True, verbose_name="Materiales usados"
    )
    fecha_mantenimiento = models.DateField(
        default=timezone.now, verbose_name="Fecha de mantenimiento"
    )
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    num_mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        db_column='num_mantenimiento',
        related_name='detalles',
        verbose_name="Mantenimiento"
    )

    class Meta:
        db_table = 'detalle_mantenimiento'
        verbose_name = "Detalle de Mantenimiento"
        verbose_name_plural = "Detalles de Mantenimiento"
        ordering = ["-fecha_mantenimiento"]

    @property
    def mantenimiento(self):
        return self.num_mantenimiento

    @mantenimiento.setter
    def mantenimiento(self, val):
        self.num_mantenimiento = val

    def __str__(self):
        return (
            f"Detalle #{self.detalle_mantenimiento} - "
            f"Mantenimiento #{self.num_mantenimiento_id}"
        )


class BitacoraEstado(models.Model):
    codigo_bitacora = models.AutoField(
        primary_key=True, db_column='codigo_bitacora'
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    estado = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Estado"
    )
    nivel_estado = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Nivel de estado"
    )
    num_mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        db_column='num_mantenimiento',
        related_name='bitacoras_estado',
        verbose_name="Mantenimiento"
    )

    class Meta:
        db_table = 'bitacora_estado'
        verbose_name = "Bitácora de Estado"
        verbose_name_plural = "Bitácoras de Estado"

    def __str__(self):
        return (
            f"Bitácora #{self.codigo_bitacora} — "
            f"Mantenimiento #{self.num_mantenimiento_id}"
        )
