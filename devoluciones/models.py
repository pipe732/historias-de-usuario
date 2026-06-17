# devoluciones/models.py
from django.db import models
from prestamo.models import DetallePrestamo   # FK principal según el MER
from herramienta.models import Herramienta    # FK directa según el MER


class DevolucionHerramienta(models.Model):
    """
    Representa la devolución de una herramienta asociada a un detalle de préstamo.

    Relaciones según el MER:
      - detalle_prestamo (FK) → tabla detalle_prestamo
      - herramienta      (FK) → tabla herramienta
    """

    detalle_prestamo = models.ForeignKey(
        DetallePrestamo,
        on_delete=models.PROTECT,
        related_name='devoluciones',
        verbose_name='Detalle de préstamo',
    )
    herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.PROTECT,
        related_name='devoluciones',
        verbose_name='Herramienta',
    )
    observaciones = models.TextField(
        blank=True,
        default='',
        verbose_name='Observaciones',
    )

    # ── Auditoría ──────────────────────────────────────────────────────────────
    fecha_creacion      = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # ── Representación ─────────────────────────────────────────────────────────
    def __str__(self):
        return (
            f"Devolución #{self.pk} — "
            f"Herramienta: {self.herramienta} — "
            f"Detalle préstamo #{self.detalle_prestamo_id}"
        )

    # ── Lógica de negocio ──────────────────────────────────────────────────────
    def aplicar(self):
        """
        Marca el detalle de préstamo como devuelto y restaura el stock
        de la herramienta en el inventario (Stock).

        Llama a actualizar_estado() en el préstamo padre para recalcular
        si el préstamo completo quedó cerrado.
        """
        detalle = self.detalle_prestamo

        # 1. Marcar el ítem como devuelto
        detalle.devuelto = True
        detalle.save(update_fields=['devuelto'])

        # 2. Restaurar stock: la cantidad a restaurar viene del detalle
        herramienta = self.herramienta
        herramienta.stock += detalle.cantidad
        herramienta.save(update_fields=['stock'])

        # 3. Recalcular estado del préstamo padre
        detalle.prestamo.actualizar_estado()

    # ── Meta ───────────────────────────────────────────────────────────────────
    class Meta:
        db_table            = 'devolucion_herramienta'   # nombre exacto del MER
        verbose_name        = 'Devolución de herramienta'
        verbose_name_plural = 'Devoluciones de herramientas'
        ordering            = ['-fecha_creacion']
        constraints = [
            # Una herramienta no puede devolverse dos veces en el mismo detalle
            models.UniqueConstraint(
                fields=['detalle_prestamo', 'herramienta'],
                name='unique_devolucion_por_detalle_herramienta',
            )
        ]    estado = models.ForeignKey(
                'bitacora.BitacoraEstado',           # ← app.Modelo de tu proyecto
                on_delete=models.PROTECT,
                related_name='prestamos',
                verbose_name='Estado',
                help_text='Estado actual del préstamo (referencia a bitácora de estados).',
            )
        