import django
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from inventario.models import Producto
from usuario.models import Usuario


class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente de aprobación'),
        ('activo',     'Activo'),
        ('parcial',    'Devuelto parcialmente'),
        ('devuelto',   'Devuelto'),
        ('vencido',    'Vencido'),
        ('rechazado',  'Rechazado'),
    ]

    # Campos del diagrama ER MySQL Workbench
    codigo_prestamo   = models.AutoField(primary_key=True, db_column='codigo_prestamo')
    observaciones     = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    estado            = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default='pendiente',
        db_index=True,
        verbose_name='Estado',
    )
    num_herramienta   = models.IntegerField(null=True, blank=True, verbose_name='Número de herramienta')
    documento         = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='documento',
        related_name='prestamos',
        verbose_name='Usuario responsable',
    )

    # Campos adicionales de gestión operativa
    nombre_usuario    = models.CharField(max_length=200, blank=True, default='', verbose_name='Nombre del responsable')
    motivo_solicitud  = models.TextField(blank=True, default='', verbose_name='Motivo de la solicitud')
    motivo_rechazo    = models.TextField(blank=True, default='', verbose_name='Motivo de rechazo')
    fecha_prestamo    = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de préstamo')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Fecha de vencimiento',
    )
    hora_max_entrega  = models.TimeField(null=True, blank=True, verbose_name='Hora máxima de entrega')

    def __init__(self, *args, **kwargs):
        if 'usuario' in kwargs:
            val = kwargs.pop('usuario')
            if isinstance(val, Usuario):
                kwargs['documento'] = val
            elif val is not None:
                try:
                    kwargs['documento'] = Usuario.objects.get(documento=str(val))
                except Exception:
                    kwargs['documento_id'] = str(val)
        super().__init__(*args, **kwargs)

    @property
    def usuario(self):
        return self.documento_id if self.documento_id else ''

    @usuario.setter
    def usuario(self, val):
        if isinstance(val, Usuario):
            self.documento = val
        elif val:
            self.documento_id = str(val)

    @property
    def usuario_id(self):
        return self.documento_id

    @property
    def esta_vencido(self):
        if not self.fecha_vencimiento:
            return False
        if self.estado == 'devuelto':
            return False
        return timezone.localdate() > self.fecha_vencimiento

    @property
    def dias_restantes(self):
        if not self.fecha_vencimiento:
            return None
        return (self.fecha_vencimiento - timezone.localdate()).days

    @property
    def tiene_items_pendientes(self):
        return self.items.filter(devuelto=False).exists()

    def actualizar_estado(self):
        items = self.items.all()
        if not items.exists():
            return
        total = items.count()
        devueltos = items.filter(devuelto=True).count()
        if devueltos == total:
            nuevo = 'devuelto'
        elif devueltos == 0:
            nuevo = 'vencido' if self.esta_vencido else 'activo'
        else:
            nuevo = 'parcial'
        if self.estado != nuevo:
            self.estado = nuevo
            self.save(update_fields=['estado', 'fecha_actualizacion'])

    def cancelar(self):
        for item in self.items.filter(devuelto=False).select_related('codigo_herramienta'):
            prod = item.codigo_herramienta
            prod.stock += item.cantidad
            prod.save(update_fields=['stock', 'actualizado_en'])
            item.devuelto = True
            item.save(update_fields=['devuelto'])
        self.estado = 'devuelto'
        self.save(update_fields=['estado', 'fecha_actualizacion'])

    def __str__(self):
        return f'Préstamo #{self.codigo_prestamo} — {self.documento_id}'

    class Meta:
        db_table            = 'prestamo'
        verbose_name        = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering            = ['-fecha_prestamo']


# DetallePrestamo (Tabla del diagrama ER Workbench)
class DetallePrestamo(models.Model):
    numero_detalle    = models.AutoField(primary_key=True, db_column='numero_detalle')
    observaciones     = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    cantidad          = models.IntegerField(default=1, verbose_name='Cantidad prestada')
    codigo_prestamo   = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='items',
        db_column='codigo_prestamo',
        verbose_name='Préstamo',
    )
    codigo_herramienta = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='items_prestamo',
        db_column='codigo_herramienta',
        verbose_name='Herramienta / Producto',
    )

    # Propiedades adicionales
    serial_entregado  = models.CharField(max_length=200, blank=True, default='', verbose_name='Serial entregado')
    devuelto          = models.BooleanField(default=False, db_index=True, verbose_name='Devuelto')

    def __init__(self, *args, **kwargs):
        if 'prestamo' in kwargs:
            kwargs['codigo_prestamo'] = kwargs.pop('prestamo')
        if 'producto' in kwargs:
            kwargs['codigo_herramienta'] = kwargs.pop('producto')
        super().__init__(*args, **kwargs)

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
        estado = '✓' if self.devuelto else '✗'
        return f'{estado} {self.codigo_herramienta} ×{self.cantidad} [Préstamo #{self.codigo_prestamo_id}]'

    class Meta:
        db_table            = 'detalle_prestamo'
        verbose_name        = 'Detalle de préstamo'
        verbose_name_plural = 'Detalles de préstamo'


# Alias para retrocompatibilidad con referencias existentes
ItemPrestamo = DetallePrestamo