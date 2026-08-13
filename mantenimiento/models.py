# mantenimiento/models.py
from django.db import models
from inventario.models import Producto
from usuario.models import Usuario

# CONSTANTES Y CHOICES CENTRALIZADOS

CATEGORIA_TIPOESTADO_CHOICES = [
    ("danado", "Dañado"),
    ("reparacion", "En reparación"),
    ("obsoleto", "Obsoleto"),
    ("calibracion", "Calibración pendiente"),
    ("preventivo", "Mantenimiento preventivo"),
    ("otro", "Otro"),
]

IMPACTO_DISPONIBILIDAD_CHOICES = [
    ("no_disponible", "No disponible"),
    ("parcialmente_disponible", "Parcialmente disponible"),
    ("disponible_restringido", "Disponible con restricción"),
]

# Nivel de severidad del estado. Pedido por el MER (campo niPreferences: Open User Settings (JSON)vel_estado).
# Sirve para ordenar/priorizar estados por gravedad real, sin depender
# del texto libre de "categoria".
NIVEL_ESTADO_CHOICES = [
    (1, "Leve"),
    (2, "Moderado"),
    (3, "Grave"),
    (4, "Crítico"),
]

TIPO_MANTENIMIENTO_CHOICES = [
    ("correctivo", "Correctivo"),
    ("preventivo", "Preventivo"),
    ("calibracion", "Calibración"),
    ("reparacion_externa", "Reparación externa"),
    ("otro", "Otro"),
]

PRIORIDAD_MANTENIMIENTO_CHOICES = [
    ("baja", "Baja"),
    ("media", "Media"),
    ("alta", "Alta"),
    ("critica", "Crítica"),
]

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

# Tipo de entrada dentro de la bitácora de detalle (detalle_mantenimiento.tipo
# en el MER). Cada fila de detalle representa UN evento en el tiempo.
TIPO_DETALLE_CHOICES = [
    ("diagnostico", "Diagnóstico"),
    ("accion", "Acción realizada"),
    ("repuesto", "Repuesto / material usado"),
    ("nota", "Nota adicional"),
    ("cierre", "Cierre / entrega"),
]

# Constantes para disponibilidad
ESTADOS_MANTENIMIENTO_ACTIVOS = {"abierto", "en_proceso"}
IMPACTO_NO_DISPONIBLE = "no_disponible"

# TIPOS DE MANTENIMIENTO

class TipoMantenimiento(models.Model):
    """
    Catálogo dinámico de tipos de mantenimiento.
    Reemplaza los choices hardcodeados para mayor flexibilidad.
    """

    nombre = models.CharField(
        max_length=50, unique=True, verbose_name="Nombre del tipo"
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    color = models.CharField(
        max_length=7, blank=True, null=True, verbose_name="Color (hex)"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tipos_mantenimiento_creados",
        verbose_name="Creado por",
    )

    class Meta:
        verbose_name = "Tipo de Mantenimiento"
        verbose_name_plural = "Tipos de Mantenimiento"
        ordering = ["nombre"]
        db_table = "mantenimiento_tipomantenimiento"

    def __str__(self):
        return self.nombre

    def puede_eliminarse(self):
        """Verifica si el tipo puede ser eliminado (nunca fue usado)."""
        return not self.mantenimientos.exists()

    def puede_inactivarse(self):
        """Verifica si puede inactivarse (sin órdenes abiertas)."""
        from django.db.models import Q

        return not self.mantenimientos.filter(
            Q(estado_registro="abierto") | Q(estado_registro="en_proceso")
        ).exists()


# TIPOS DE ESTADO
class TipoEstado(models.Model):
    # Se usan las constantes a nivel de módulo: CATEGORIA_TIPOESTADO_CHOICES,
    # IMPACTO_DISPONIBILIDAD_CHOICES y NIVEL_ESTADO_CHOICES para evitar duplicación.
    nombre = models.CharField(
        max_length=120, unique=True, verbose_name="Nombre del estado"
    )
    codigo = models.CharField(
        max_length=20, unique=True, verbose_name="Código abreviado"
    )
    descripcion = models.TextField(
        blank=True, null=True, verbose_name="Descripción breve"
    )
    categoria = models.CharField(
        max_length=50, choices=CATEGORIA_TIPOESTADO_CHOICES, verbose_name="Categoría"
    )
    # Campo pedido por el MER (bitácora_estado.nivel_estado). Permite
    # ordenar/filtrar estados por severidad sin parsear texto de "categoria".
    nivel_estado = models.PositiveSmallIntegerField(
        choices=NIVEL_ESTADO_CHOICES,
        default=1,
        verbose_name="Nivel de severidad",
    )
    impacto_disponibilidad = models.CharField(
        max_length=40,
        choices=IMPACTO_DISPONIBILIDAD_CHOICES,
        default=IMPACTO_NO_DISPONIBLE,
        verbose_name="Impacto en disponibilidad",
    )
    color = models.CharField(max_length=7, blank=True, verbose_name="Color asociado")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Tipo de Estado"
        verbose_name_plural = "Tipos de Estado"
        ordering = ["nombre"]
        db_table = "mantenimiento_tipoestado"


# registro de mantenimiento (cabecera — equivale a bitácora_mantenimiento del MER)
class Mantenimiento(models.Model):
    """
    Cabecera del mantenimiento. Guarda QUÉ se está atendiendo, de qué tipo,
    con qué estado y prioridad. El detalle día a día (diagnóstico, acciones,
    repuestos, notas) vive en DetalleMantenimiento, no aquí.
    """

    # Relaciones
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="mantenimientos",
        verbose_name="Ítem / Herramienta",
    )
    tipo_mantenimiento = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        related_name="mantenimientos",
        verbose_name="Tipo de mantenimiento",
    )
    tipo_estado = models.ForeignKey(
        TipoEstado,
        on_delete=models.PROTECT,
        related_name="mantenimientos",
        verbose_name="Tipo de estado actual",
    )
    responsable = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        related_name="mantenimientos_responsable",
        verbose_name="Responsable / Técnico",
    )
    creado_por = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        related_name="mantenimientos_creados",
        verbose_name="Registrado por",
    )

    # Campos de cabecera
    estado_registro = models.CharField(
        max_length=20,
        choices=ESTADO_REGISTRO_CHOICES,
        default="abierto",
        verbose_name="Estado del registro",
    )
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_MANTENIMIENTO_CHOICES,
        default="media",
        verbose_name="Prioridad / urgencia",
    )
    fecha_reporte = models.DateField(verbose_name="Fecha de reporte / detección")
    fecha_inicio = models.DateField(verbose_name="Fecha inicio mantenimiento")
    fecha_fin_estimada = models.DateField(
        blank=True, null=True, verbose_name="Fecha estimada de entrega"
    )
    fecha_fin_real = models.DateField(
        blank=True, null=True, verbose_name="Fecha entrega real"
    )
    tiempo_empleado_horas = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Tiempo empleado (horas)",
    )
    ubicacion_snapshot = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Ubicación al momento del registro",
    )
    costo_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Costo estimado",
    )
    costo_real = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Costo real",
    )
    actualizado_por = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mantenimientos_actualizados",
        verbose_name="Última edición por",
    )

    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validaciones de integridad del modelo."""
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.utils.translation import gettext_lazy as _

        errors = {}

        if (
            self.fecha_fin_estimada
            and self.fecha_inicio
            and self.fecha_fin_estimada < self.fecha_inicio
        ):
            errors["fecha_fin_estimada"] = _(
                "La fecha estimada debe ser posterior a la de inicio."
            )

        if (
            self.fecha_fin_real
            and self.fecha_fin_estimada
            and self.fecha_fin_real > self.fecha_fin_estimada
        ):
            # Nota: Permitimos retrasos, solo advertencia en logs
            pass

        if self.tiempo_empleado_horas and self.tiempo_empleado_horas < 0:
            errors["tiempo_empleado_horas"] = _("El tiempo no puede ser negativo.")

        if self.costo_estimado and self.costo_estimado < 0:
            errors["costo_estimado"] = _("El costo estimado no puede ser negativo.")

        if self.costo_real and self.costo_real < 0:
            errors["costo_real"] = _("El costo real no puede ser negativo.")

        if errors:
            raise DjangoValidationError(errors)

    @staticmethod
    def _calcular_disponibilidad_producto(producto):
        """
        Un producto queda no disponible si existe al menos un mantenimiento
        activo (abierto/en_proceso) con impacto no_disponible.
        """
        bloqueo = Mantenimiento.objects.filter(
            producto=producto,
            estado_registro__in=ESTADOS_MANTENIMIENTO_ACTIVOS,
            tipo_estado__impacto_disponibilidad=IMPACTO_NO_DISPONIBLE,
        ).exists()
        return not bloqueo

    def _actualizar_disponibilidad(self):
        if not self.producto_id:
            return

        disponible = self._calcular_disponibilidad_producto(self.producto)
        if self.producto.disponible != disponible:
            self.producto.disponible = disponible
            self.producto.save(update_fields=["disponible"])

    def save(self, *args, **kwargs):
        # Snapshot de ubicación
        if not self.pk and self.producto_id and self.producto.ubicacion:
            self.ubicacion_snapshot = self.producto.ubicacion

        super().save(*args, **kwargs)
        self._actualizar_disponibilidad()

    def delete(self, *args, **kwargs):
        producto = self.producto if self.producto_id else None
        super().delete(*args, **kwargs)
        if producto:
            producto.disponible = self._calcular_disponibilidad_producto(producto)
            producto.save(update_fields=["disponible"])

    def __str__(self):
        return f"[{self.tipo_mantenimiento}] {self.producto} — {self.fecha_reporte}"

    def registrar_cambio(
        self, *, editado_por, motivo_edicion, cambios, detalle_motivo=""
    ):
        if not cambios:
            return None
        return MantenimientoCambio.objects.create(
            mantenimiento=self,
            editado_por=editado_por,
            motivo_edicion=motivo_edicion,
            detalle_motivo=detalle_motivo,
            cambios=cambios,
        )

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha_reporte"]
        db_table = "mantenimiento_bitacoramantenimiento"


# detalle_mantenimiento del MER. Historial de eventos de UN mantenimiento.
# Antes estos campos (descripcion_problema, acciones_realizadas,
# materiales_usados, notas_adicionales, evidencia_adicional) vivían sueltos
# dentro de Mantenimiento. Separarlos permite VARIOS registros en el tiempo
# por mantenimiento, en vez de un solo bloque de texto fijo.
class DetalleMantenimiento(models.Model):
    mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="Mantenimiento",
    )
    # El MER repite tipo_mantenimiento(fk) también en el detalle. Se conserva
    # para no romper el diagrama, pero normalmente coincidirá con el de la
    # cabecera; útil solo si un detalle puntual cambia de tipo (ej. pasa de
    # correctivo a calibración a mitad de proceso).
    tipo_mantenimiento = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        related_name="detalles_mantenimiento",
        verbose_name="Tipo de mantenimiento (detalle)",
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_DETALLE_CHOICES,
        verbose_name="Tipo de entrada",
    )
    descripcion = models.TextField(verbose_name="Descripción")
    evidencia_adicional = models.FileField(
        upload_to="mantenimiento/evidencias/",
        blank=True,
        null=True,
        verbose_name="Evidencia adjunta",
    )
    registrado_por = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="detalles_mantenimiento_creados",
        verbose_name="Registrado por",
    )
    creado_en = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha del evento"
    )

    class Meta:
        verbose_name = "Detalle de Mantenimiento"
        verbose_name_plural = "Detalles de Mantenimiento"
        ordering = ["creado_en"]
        db_table = "mantenimiento_detallemantenimiento"

    def __str__(self):
        return f"Detalle #{self.pk} ({self.get_tipo_display()}) - OT #{self.mantenimiento_id}"

class MantenimientoCambio(models.Model):
    mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        related_name="cambios_auditoria",
        verbose_name="Mantenimiento",
    )
    editado_por = models.ForeignKey(
        "usuario.Usuario",  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cambios_mantenimiento",
        verbose_name="Editado por",
    )
    fecha_edicion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de edición"
    )
    motivo_edicion = models.CharField(
        max_length=40, choices=MOTIVO_CAMBIO_CHOICES, verbose_name="Motivo de edición"
    )
    detalle_motivo = models.CharField(
        max_length=255, blank=True, verbose_name="Detalle del motivo"
    )
    cambios = models.JSONField(default=dict, verbose_name="Campos modificados")

    class Meta:
        verbose_name = "Cambio de mantenimiento"
        verbose_name_plural = "Cambios de mantenimiento"
        ordering = ["-fecha_edicion"]

    def __str__(self):
        return f"Cambio OT #{self.mantenimiento_id} - {self.fecha_edicion:%Y-%m-%d %H:%M}"

    def get_editado_por_nombre(self):
        if not self.editado_por:
            return "Sistema"
        return self.editado_por.nombre_completo if hasattr(self.editado_por, 'nombre_completo') else \
            self.editado_por.get_full_name() or self.editado_por.username
"""            
class Empresa(models.Model):
    proveedor = models.OneToOneField = ()
"""

