from django.db import models
from django.utils import timezone
from inventario.models import Producto
from usuario.models import Usuario

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

TIPO_DETALLE_CHOICES = [
    ("diagnostico", "Diagnóstico"),
    ("accion", "Acción realizada"),
    ("repuesto", "Repuesto / material usado"),
    ("nota", "Nota adicional"),
    ("cierre", "Cierre / entrega"),
]

ESTADOS_MANTENIMIENTO_ACTIVOS = {"abierto", "en_proceso"}
IMPACTO_NO_DISPONIBLE = "no_disponible"


class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del tipo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    color = models.CharField(max_length=7, blank=True, null=True, verbose_name="Color (hex)")
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


class TipoEstado(models.Model):
    nombre = models.CharField(max_length=120, unique=True, verbose_name="Nombre del estado")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código abreviado")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción breve")
    categoria = models.CharField(max_length=50, choices=CATEGORIA_TIPOESTADO_CHOICES, verbose_name="Categoría")
    nivel_estado = models.PositiveSmallIntegerField(choices=NIVEL_ESTADO_CHOICES, default=1, verbose_name="Nivel de severidad")
    impacto_disponibilidad = models.CharField(
        max_length=40,
        choices=IMPACTO_DISPONIBILIDAD_CHOICES,
        default=IMPACTO_NO_DISPONIBLE,
        verbose_name="Impacto en disponibilidad",
    )
    color = models.CharField(max_length=7, blank=True, verbose_name="Color asociado")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Creado por")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Tipo de Estado"
        verbose_name_plural = "Tipos de Estado"
        ordering = ["nombre"]
        db_table = "mantenimiento_tipoestado"


# Mantenimiento (Tabla del diagrama ER Workbench)
class Mantenimiento(models.Model):
    num_mantenimiento = models.AutoField(primary_key=True, db_column='num_mantenimiento')
    tipo_mantenimiento = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        related_name="mantenimientos",
        verbose_name="Tipo de mantenimiento",
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_reporte = models.DateField(default=timezone.now, verbose_name="Fecha de reporte / detección")
    fecha_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de inicio del mantenimiento")
    fecha_fin_real = models.DateField(blank=True, null=True, verbose_name="Fecha de fin real / entrega")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    codigo_herramienta = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mantenimientos",
        db_column="codigo_herramienta",
        verbose_name="Ítem / Herramienta",
    )

    # Campos adicionales de gestión operativa
    tipo_estado = models.ForeignKey(
        TipoEstado,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mantenimientos",
        verbose_name="Tipo de estado actual",
    )
    responsable = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mantenimientos_responsable",
        verbose_name="Responsable / Técnico",
    )
    creado_por = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mantenimientos_creados",
        verbose_name="Registrado por",
    )
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
    fecha_fin_estimada = models.DateField(blank=True, null=True, verbose_name="Fecha estimada de entrega")
    tiempo_empleado_horas = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name="Tiempo empleado (horas)")
    ubicacion_snapshot = models.CharField(max_length=150, blank=True, null=True, verbose_name="Ubicación al momento del registro")
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Costo estimado")
    costo_real = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Costo real")
    actualizado_por = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mantenimientos_actualizados",
        verbose_name="Última edición por",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def registrar_cambio(self, *, editado_por, motivo_edicion, cambios, detalle_motivo=""):
        if not cambios:
            return None
        return MantenimientoCambio.objects.create(
            mantenimiento=self,
            editado_por=editado_por,
            motivo_edicion=motivo_edicion,
            detalle_motivo=detalle_motivo,
            cambios=cambios,
        )

    def clean(self):
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.utils.translation import gettext_lazy as _

        errors = {}

        if self.fecha_inicio and self.fecha_reporte and self.fecha_inicio < self.fecha_reporte:
            errors["fecha_inicio"] = _("La fecha de inicio no puede ser anterior a la fecha de reporte.")

        fecha_base = self.fecha_inicio or self.fecha_reporte
        if self.fecha_fin_estimada and fecha_base and self.fecha_fin_estimada < fecha_base:
            errors["fecha_fin_estimada"] = _(
                "La fecha estimada no puede ser anterior a la fecha de inicio o reporte."
            )

        if self.fecha_fin_real and fecha_base and self.fecha_fin_real < fecha_base:
            errors["fecha_fin_real"] = _(
                "La fecha real no puede ser anterior a la fecha de inicio o reporte."
            )

        if self.tiempo_empleado_horas is not None and self.tiempo_empleado_horas < 0:
            errors["tiempo_empleado_horas"] = _("El tiempo no puede ser negativo.")
        if self.costo_estimado is not None and self.costo_estimado < 0:
            errors["costo_estimado"] = _("El costo estimado no puede ser negativo.")
        if self.costo_real is not None and self.costo_real < 0:
            errors["costo_real"] = _("El costo real no puede ser negativo.")

        if errors:
            raise DjangoValidationError(errors)

    def _actualizar_disponibilidad(self):
        if not self.codigo_herramienta_id:
            return
        bloqueo = Mantenimiento.objects.filter(
            codigo_herramienta=self.codigo_herramienta,
            estado_registro__in=ESTADOS_MANTENIMIENTO_ACTIVOS,
            tipo_estado__impacto_disponibilidad=IMPACTO_NO_DISPONIBLE,
        ).exists()
        disponible = not bloqueo
        if self.codigo_herramienta.disponible != disponible:
            self.codigo_herramienta.disponible = disponible
            self.codigo_herramienta.save(update_fields=["disponible"])

    def save(self, *args, **kwargs):
        if not self.pk and self.codigo_herramienta_id and self.codigo_herramienta.ubicacion:
            self.ubicacion_snapshot = self.codigo_herramienta.ubicacion
        super().save(*args, **kwargs)
        self._actualizar_disponibilidad()

    def delete(self, *args, **kwargs):
        prod = self.codigo_herramienta
        super().delete(*args, **kwargs)
        if prod:
            bloqueo = Mantenimiento.objects.filter(
                codigo_herramienta=prod,
                estado_registro__in=ESTADOS_MANTENIMIENTO_ACTIVOS,
                tipo_estado__impacto_disponibilidad=IMPACTO_NO_DISPONIBLE,
            ).exists()
            disponible = not bloqueo
            if prod.disponible != disponible:
                prod.disponible = disponible
                prod.save(update_fields=["disponible"])

    def __str__(self):
        return f"[{self.tipo_mantenimiento}] {self.codigo_herramienta} — {self.fecha_reporte}"

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha_reporte"]
        db_table = "mantenimiento"


# DetalleMantenimiento (Tabla del diagrama ER Workbench)
class DetalleMantenimiento(models.Model):
    detalle_mantenimiento = models.AutoField(primary_key=True, db_column='detalle_mantenimiento')
    accion_realizada = models.TextField(blank=True, null=True, verbose_name="Acción realizada")
    materiales_usados = models.TextField(blank=True, null=True, verbose_name="Materiales usados")
    fecha_mantenimiento = models.DateField(default=timezone.now, verbose_name="Fecha de mantenimiento")
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    num_mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="detalles",
        db_column="num_mantenimiento",
        verbose_name="Mantenimiento",
    )

    # Campos adicionales de soporte
    tipo_mantenimiento = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="detalles_mantenimiento",
        verbose_name="Tipo de mantenimiento (detalle)",
    )
    tipo = models.CharField(max_length=20, choices=TIPO_DETALLE_CHOICES, default="diagnostico", verbose_name="Tipo de entrada")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    evidencia_adicional = models.FileField(upload_to="mantenimiento/evidencias/", blank=True, null=True, verbose_name="Evidencia adjunta")
    registrado_por = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="detalles_mantenimiento_creados",
        verbose_name="Registrado por",
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del evento")

    @property
    def mantenimiento(self):
        return self.num_mantenimiento

    @mantenimiento.setter
    def mantenimiento(self, val):
        self.num_mantenimiento = val

    class Meta:
        verbose_name = "Detalle de Mantenimiento"
        verbose_name_plural = "Detalles de Mantenimiento"
        ordering = ["creado_en"]
        db_table = "detalle_mantenimiento"

    def __str__(self):
        return f"Detalle #{self.pk} - Mantenimiento #{self.num_mantenimiento_id}"


# BitacoraEstado (Tabla del diagrama ER Workbench)
class BitacoraEstado(models.Model):
    codigo_bitacora = models.AutoField(primary_key=True, db_column='codigo_bitacora')
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    estado = models.CharField(max_length=50, verbose_name="Estado")
    nivel_estado = models.CharField(max_length=50, verbose_name="Nivel de estado")
    num_mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="bitacoras_estado",
        db_column="num_mantenimiento",
        verbose_name="Mantenimiento",
    )

    class Meta:
        verbose_name = "Bitácora de Estado"
        verbose_name_plural = "Bitácoras de Estado"
        db_table = "bitacora_estado"

    def __str__(self):
        return f"Bitácora #{self.codigo_bitacora} — Mantenimiento #{self.num_mantenimiento_id}"


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
    fecha_edicion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de edición")
    motivo_edicion = models.CharField(max_length=40, choices=MOTIVO_CAMBIO_CHOICES, verbose_name="Motivo de edición")
    detalle_motivo = models.CharField(max_length=255, blank=True, verbose_name="Detalle del motivo")
    cambios = models.JSONField(default=dict, verbose_name="Campos modificados")

    class Meta:
        verbose_name = "Cambio de mantenimiento"
        verbose_name_plural = "Cambios de mantenimiento"
        ordering = ["-fecha_edicion"]

    def __str__(self):
        return f"Cambio OT #{self.mantenimiento_id} - {self.fecha_edicion:%Y-%m-%d %H:%M}"
