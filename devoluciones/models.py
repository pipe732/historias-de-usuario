from django.db import models
from prestamo.models import Prestamo, DetallePrestamo
from usuario.models import Usuario


# DevolucionHerramienta (Tabla del diagrama ER Workbench)
class DevolucionHerramienta(models.Model):
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

    codigo_devolucion = models.AutoField(primary_key=True, db_column='codigo_devolucion')
    observaciones     = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    fecha             = models.DateField(auto_now_add=True, verbose_name='Fecha de devolución')
    codigo_prestamo   = models.ForeignKey(
        Prestamo,
        on_delete=models.PROTECT,
        related_name='devoluciones',
        db_column='codigo_prestamo',
        verbose_name='Préstamo',
    )
    codigo_recibe     = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='codigo_recibe',
        related_name='devoluciones_recibidas',
        verbose_name='Usuario que recibe',
    )

    # Campos de soporte operativo
    items = models.ManyToManyField(
        DetallePrestamo,
        related_name='devoluciones',
        verbose_name='Ítems devueltos',
        blank=True,
    )
    devolucion_total = models.BooleanField(
        default=True,
        help_text='True = todas las herramientas; False = devolución parcial'
    )
    motivo = models.TextField(blank=True, null=True, verbose_name='Motivo')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    estado_equipo = models.CharField(
        max_length=30,
        choices=ESTADO_EQUIPO_CHOICES,
        default='excelente',
        verbose_name='Estado de la herramienta'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    @property
    def id(self):
        return self.codigo_devolucion

    @property
    def prestamo(self):
        return self.codigo_prestamo

    @prestamo.setter
    def prestamo(self, val):
        self.codigo_prestamo = val

    def aplicar(self, cantidades=None):
        from inventario.models import MovimientoKardex
        for item in self.items.select_related('codigo_herramienta'):
            item.devuelto = True
            item.save(update_fields=['devuelto'])
            cant = cantidades.get(item.pk, item.cantidad) if (cantidades and item.pk in cantidades) else item.cantidad
            prod = item.codigo_herramienta
            stock_ant = prod.stock
            prod.stock += cant
            prod.save(update_fields=['stock', 'actualizado_en'])

            try:
                MovimientoKardex.objects.create(
                    producto=prod,
                    tipo_movimiento='devolucion',
                    cantidad=cant,
                    stock_anterior=stock_ant,
                    stock_nuevo=prod.stock,
                    usuario_nombre=f"{self.codigo_prestamo.nombre_usuario or self.codigo_prestamo.documento_id}",
                    observaciones=f"Devolución #{self.codigo_devolucion} (Estado: {self.get_estado_equipo_display()})"
                )
            except Exception:
                pass
        self.codigo_prestamo.actualizar_estado()

    def __str__(self):
        tipo = "total" if self.devolucion_total else "parcial"
        return f"Devolución #{self.codigo_devolucion} ({tipo}) — Préstamo #{self.codigo_prestamo_id}"

    class Meta:
        db_table            = 'devolucion_herramienta'
        verbose_name        = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        ordering            = ['-fecha_creacion']


# Alias para retrocompatibilidad con referencias existentes
Devolucion = DevolucionHerramienta
