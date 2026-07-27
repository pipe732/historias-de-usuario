# devoluciones/models.py
from django.db import models
from prestamo.models import Prestamo, ItemPrestamo

class Devolucion(models.Model):
    ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobada',  'Aprobada'),
    ('rechazada', 'Rechazada'),
]

    ESTADO_EQUIPO_CHOICES = [
        ('excelente', 'Excelente'),
        ('limpieza', 'Requiere Limpieza'),
        ('mantenimiento', 'Requiere Mantenimiento'),
        ('danado', 'Dañado / Defectuoso'),
    ]

    prestamo = models.ForeignKey(
                    Prestamo,
                    on_delete=models.PROTECT,
                    related_name='devoluciones',
                    verbose_name='Préstamo'
                )
    items   = models.ManyToManyField(
                    ItemPrestamo,
                    related_name='devoluciones',
                    verbose_name='Ítems devueltos',
                    blank=True,
                )
    devolucion_total = models.BooleanField(
                        default=True,
                        help_text='True = todas las herramientas; False = devolución parcial'
                    )
    motivo           = models.TextField()
    estado           = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    estado_equipo    = models.CharField(max_length=30, choices=ESTADO_EQUIPO_CHOICES, default='excelente', verbose_name='Estado de la herramienta')
    fecha_creacion      = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        tipo = "total" if self.devolucion_total else "parcial"
        return f"Devolución #{self.id} ({tipo}) — Préstamo #{self.prestamo_id}"

    def aplicar(self, cantidades=None):
        """
        Marca los ítems seleccionados como devueltos,
        restaura el stock en inventario y recalcula estado del préstamo.
        """
        from inventario.models import MovimientoKardex
        for item in self.items.select_related('producto'):
            item.devuelto = True
            item.save(update_fields=['devuelto'])
            # Restaurar stock al inventario
            cant = cantidades.get(item.pk, item.cantidad) if (cantidades and item.pk in cantidades) else item.cantidad
            stock_ant = item.producto.stock
            item.producto.stock += cant
            item.producto.save(update_fields=['stock', 'actualizado_en'])

            try:
                MovimientoKardex.objects.create(
                    producto=item.producto,
                    tipo_movimiento='devolucion',
                    cantidad=cant,
                    stock_anterior=stock_ant,
                    stock_nuevo=item.producto.stock,
                    usuario_nombre=f"{self.prestamo.nombre_usuario or self.prestamo.usuario}",
                    observaciones=f"Devolución #{self.id} (Estado: {self.get_estado_equipo_display()})"
                )
            except Exception:
                pass
        self.prestamo.actualizar_estado()

    class Meta:
        verbose_name        = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        ordering            = ['-fecha_creacion']
