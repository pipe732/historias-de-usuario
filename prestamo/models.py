from django.db import models
from django.utils import timezone
from inventario.models import Herramienta, Producto
from usuario.models import Usuario


class Prestamo(models.Model):
    codigo_prestamo = models.AutoField(primary_key=True, db_column='codigo_prestamo')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    estado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Estado')
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha de préstamo')
    documento = models.ForeignKey(
        Usuario,
        on_delete=models.RESTRICT,
        db_column='documento',
        related_name='prestamos',
        verbose_name='Usuario responsable',
    )

    class Meta:
        db_table = 'prestamo'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-fecha']

    @property
    def usuario(self):
        return self.documento

    @usuario.setter
    def usuario(self, val):
        self.documento = val

    @property
    def nombre_usuario(self):
        return self.documento.nombre_completo if self.documento else ''

    @nombre_usuario.setter
    def nombre_usuario(self, val):
        pass

    @property
    def usuario_id(self):
        return self.documento_id

    @property
    def fecha_prestamo(self):
        return self.fecha

    @fecha_prestamo.setter
    def fecha_prestamo(self, val):
        self.fecha = val

    def __str__(self):
        return f'Préstamo #{self.codigo_prestamo} — {self.documento_id}'


class DetallePrestamo(models.Model):
    numero_detalle = models.AutoField(primary_key=True, db_column='numero_detalle')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    cantidad = models.IntegerField(default=1, verbose_name='Cantidad')
    codigo_prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        db_column='codigo_prestamo',
        related_name='items',
        verbose_name='Préstamo',
    )
    codigo_herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.RESTRICT,
        db_column='codigo_herramienta',
        related_name='detalles_prestamo',
        verbose_name='Herramienta',
    )

    class Meta:
        db_table = 'detalle_prestamo'
        verbose_name = 'Detalle de préstamo'
        verbose_name_plural = 'Detalles de préstamo'

    @property
    def prestamo(self):
        return self.codigo_prestamo

    @prestamo.setter
    def prestamo(self, val):
        self.codigo_prestamo = val

    @property
    def producto(self):
        return self.codigo_herramienta

    @producto.setter
    def producto(self, val):
        self.codigo_herramienta = val

    def __str__(self):
        return f'Detalle #{self.numero_detalle} - Herramienta #{self.codigo_herramienta_id} ×{self.cantidad}'


# Alias para retrocompatibilidad
ItemPrestamo = DetallePrestamo