from django.db import models
from django.utils import timezone
from prestamo.models import Prestamo
from usuario.models import Usuario


class DevolucionHerramienta(models.Model):
    codigo_devolucion = models.AutoField(primary_key=True, db_column='codigo_devolucion')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha de devolución')
    codigo_prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.RESTRICT,
        db_column='codigo_prestamo',
        related_name='devoluciones',
        verbose_name='Préstamo',
    )
    codigo_recibe = models.ForeignKey(
        Usuario,
        on_delete=models.RESTRICT,
        db_column='codigo_recibe',
        related_name='devoluciones_recibidas',
        verbose_name='Usuario que recibe',
    )

    class Meta:
        db_table = 'devolucion_herramientas'
        verbose_name = 'Devolución de Herramienta'
        verbose_name_plural = 'Devoluciones de Herramientas'
        ordering = ['-fecha']

    @property
    def prestamo(self):
        return self.codigo_prestamo

    @prestamo.setter
    def prestamo(self, val):
        self.codigo_prestamo = val

    @property
    def usuario_recibe(self):
        return self.codigo_recibe

    @usuario_recibe.setter
    def usuario_recibe(self, val):
        self.codigo_recibe = val

    def __str__(self):
        return f"Devolución #{self.codigo_devolucion} — Préstamo #{self.codigo_prestamo_id}"


# Alias para retrocompatibilidad
Devolucion = DevolucionHerramienta
