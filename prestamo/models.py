# prestamo/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# ---------------------------------------------------------------------------
# Entidades de soporte (referenciadas por préstamo)
# ---------------------------------------------------------------------------

class BitacoraEstado(models.Model):
    """Catálogo de estados posibles para un préstamo."""

    descripcion  = models.CharField(max_length=200, verbose_name='Descripción')
    estado       = models.CharField(max_length=100, verbose_name='Estado')
    nivel_estado = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='Nivel de estado',
        help_text='Ej: info, warning, danger',
    )

    def __str__(self):
        return f'{self.estado} — {self.descripcion}'

    class Meta:
        verbose_name        = 'Bitácora de estado'
        verbose_name_plural = 'Bitácoras de estado'
        ordering            = ['estado']


class Usuario(models.Model):
    """Aprendiz o persona que solicita un préstamo."""

    TIPO_DOC_CHOICES = [
        ('CC',  'Cédula de ciudadanía'),
        ('TI',  'Tarjeta de identidad'),
        ('CE',  'Cédula de extranjería'),
        ('PA',  'Pasaporte'),
        ('NUIP','NUIP'),
    ]

    ROL_CHOICES = [
        ('aprendiz',    'Aprendiz'),
        ('instructor',  'Instructor'),
        ('funcionario', 'Funcionario'),
    ]

    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de documento',
    )
    id_rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='aprendiz',
        verbose_name='Rol',
    )
    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre completo')
    correo          = models.EmailField(blank=True, default='', verbose_name='Correo')
    telefono        = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='Teléfono',
    )
    tipo_documento  = models.CharField(
        max_length=10,
        choices=TIPO_DOC_CHOICES,
        default='CC',
        verbose_name='Tipo de documento',
    )

    def __str__(self):
        return f'{self.nombre_completo} ({self.numero_documento})'

    class Meta:
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering            = ['nombre_completo']


# ---------------------------------------------------------------------------
# Préstamo
# ---------------------------------------------------------------------------

class Prestamo(models.Model):
    """
    Registro principal de un préstamo de herramientas.

    Relaciones según el MER:
    - usuario (numero_documento) → Usuario
    - id_estado                  → BitacoraEstado
    - genera                     → DetallePrestamo  (acceso por related_name='detalles')
    - originada                  → DevolucionHerramienta (acceso por related_name='devoluciones')
    """

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='prestamos',
        to_field='numero_documento',
        verbose_name='Usuario (documento)',
    )
    id_estado = models.ForeignKey(
        BitacoraEstado,
        on_delete=models.PROTECT,
        related_name='prestamos',
        verbose_name='Estado',
    )
    observaciones = models.TextField(
        blank=True,
        default='',
        verbose_name='Observaciones',
    )

    # Auditoría
    fecha_prestamo      = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de préstamo')
    fecha_actualizacion = models.DateTimeField(auto_now=True,     verbose_name='Última actualización')

    # ── Validaciones ────────────────────────────────────────────────────
    def clean(self):
        super().clean()
        errors = {}
        if not self.usuario_id:
            errors['usuario'] = 'Debe indicar el usuario del préstamo.'
        if errors:
            raise ValidationError(errors)

    # ── Propiedades calculadas ──────────────────────────────────────────
    @property
    def tiene_items_pendientes(self):
        return self.detalles.filter(devolucion__isnull=True).exists()

    # ── Representación ──────────────────────────────────────────────────
    def __str__(self):
        return f'Préstamo #{self.pk} — {self.usuario}'

    class Meta:
        verbose_name        = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering            = ['-fecha_prestamo']


# ---------------------------------------------------------------------------
# Herramienta (referenciada por DetallePrestamo)
# ---------------------------------------------------------------------------

class CategoriaHerramienta(models.Model):
    tipo_herramienta = models.CharField(max_length=100, verbose_name='Tipo de herramienta')
    descripcion      = models.TextField(blank=True, default='', verbose_name='Descripción')

    def __str__(self):
        return self.tipo_herramienta

    class Meta:
        verbose_name        = 'Categoría de herramienta'
        verbose_name_plural = 'Categorías de herramienta'


class Herramienta(models.Model):
    """Herramienta física disponible para préstamo."""

    categoria   = models.ForeignKey(
        CategoriaHerramienta,
        on_delete=models.PROTECT,
        related_name='herramientas',
        verbose_name='Categoría',
    )
    nombre_herramienta = models.CharField(max_length=200, verbose_name='Nombre')
    descripcion        = models.TextField(blank=True, default='', verbose_name='Descripción')

    def __str__(self):
        return self.nombre_herramienta

    class Meta:
        verbose_name        = 'Herramienta'
        verbose_name_plural = 'Herramientas'
        ordering            = ['nombre_herramienta']


# ---------------------------------------------------------------------------
# Detalle de préstamo
# ---------------------------------------------------------------------------

class DetallePrestamo(models.Model):
    """
    Línea de detalle: qué herramienta y cuántas unidades se prestan
    dentro de un Prestamo.

    Relaciones según el MER:
    - id_prestamo    → Prestamo
    - id_herramienta → Herramienta
    - genera         → DevolucionHerramienta (acceso por related_name='devolucion')
    """

    prestamo    = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Préstamo',
    )
    herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.PROTECT,
        related_name='detalles_prestamo',
        verbose_name='Herramienta',
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad prestada',
    )

    # ── Validaciones ────────────────────────────────────────────────────
    def clean(self):
        super().clean()
        if self.cantidad < 1:
            raise ValidationError({'cantidad': 'La cantidad debe ser al menos 1.'})

    # ── Propiedades ─────────────────────────────────────────────────────
    @property
    def esta_devuelto(self):
        """True si existe una devolución asociada a este detalle."""
        return hasattr(self, 'devolucion') and self.devolucion is not None

    def __str__(self):
        estado = '✓' if self.esta_devuelto else '✗'
        return f'{estado} {self.herramienta} ×{self.cantidad} [{self.prestamo}]'

    class Meta:
        verbose_name        = 'Detalle de préstamo'
        verbose_name_plural = 'Detalles de préstamo'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gte=1),
                name='detalleprestamo_cantidad_gte_1',
            )
        ]


# ---------------------------------------------------------------------------
# Devolución de herramienta
# ---------------------------------------------------------------------------

class DevolucionHerramienta(models.Model):
    """
    Registro de la devolución de una herramienta prestada.
    Se origina desde un DetallePrestamo (relación 1-a-1).
    """

    detalle_prestamo = models.OneToOneField(
        DetallePrestamo,
        on_delete=models.CASCADE,
        related_name='devolucion',
        verbose_name='Detalle de préstamo',
    )
    herramienta = models.ForeignKey(
        Herramienta,
        on_delete=models.PROTECT,
        related_name='devoluciones',
        verbose_name='Herramienta devuelta',
    )
    observaciones     = models.TextField(blank=True, default='', verbose_name='Observaciones')
    fecha_devolucion  = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de devolución')

    def __str__(self):
        return f'Devolución de {self.herramienta} — {self.detalle_prestamo}'

    class Meta:
        verbose_name        = 'Devolución de herramienta'
        verbose_name_plural = 'Devoluciones de herramienta'
        ordering            = ['-fecha_devolucion']