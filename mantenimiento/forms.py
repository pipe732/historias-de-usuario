# mantenimiento/forms.py
from django import forms
from django.core.exceptions import ValidationError
from usuario.models import Usuario

from .models import (
    TipoEstado,
    TipoMantenimiento,
    Mantenimiento,
    DetalleMantenimiento,
    MantenimientoCambio,
    MOTIVO_CAMBIO_CHOICES,
)
from inventario.models import Producto


# ==================== TIPO MANTENIMIENTO ====================

class TipoMantenimientoForm(forms.ModelForm):
    """Formulario para crear y editar tipos de mantenimiento."""

    class Meta:
        model = TipoMantenimiento
        fields = ["nombre", "descripcion", "color"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Correctivo, Preventivo...",
                    "maxlength": "50",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descripción del tipo de mantenimiento (opcional)",
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                    "style": "max-width: 100px;",
                }
            ),
        }
        labels = {
            "nombre": "Nombre del tipo",
            "descripcion": "Descripción",
            "color": "Color (opcional)",
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre:
            qs = TipoMantenimiento.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe un tipo de mantenimiento con este nombre.")
        return nombre


# ==================== TIPO ESTADO ====================

class TipoEstadoForm(forms.ModelForm):

    class Meta:
        model = TipoEstado
        fields = [
            "nombre",
            "codigo",
            "descripcion",
            "categoria",
            "nivel_estado",
            "impacto_disponibilidad",
            "color",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Dañado severo"}
            ),
            "codigo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: DS"}
            ),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "nivel_estado": forms.Select(attrs={"class": "form-select"}),
            "impacto_disponibilidad": forms.Select(attrs={"class": "form-select"}),
            "color": forms.TextInput(
                attrs={"type": "color", "class": "form-control form-control-color w-25"}
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre:
            qs = TipoEstado.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe un tipo de estado con este nombre.")
        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")
        if codigo:
            qs = TipoEstado.objects.filter(codigo__iexact=codigo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Este código ya está en uso.")
        return codigo


# ==================== MANTENIMIENTO ====================

class MantenimientoForm(forms.ModelForm):
    producto_busqueda = forms.CharField(
        required=False,
        label="Ítem / Herramienta",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar por código, nombre o serie...",
                "id": "producto_busqueda",
                "autocomplete": "off",
                "aria-label": "Búsqueda de ítem o herramienta",
            }
        ),
    )

    class Meta:
        model = Mantenimiento
        fields = [
            "producto",
            "tipo_mantenimiento",
            "tipo_estado",
            "fecha_reporte",
            "fecha_inicio",
            "fecha_fin_estimada",
            "fecha_fin_real",
            "tiempo_empleado_horas",
            "prioridad",
            "responsable",
            "costo_estimado",
            "costo_real",
            "estado_registro"
        ]
        widgets = {
            "producto": forms.HiddenInput(),
            "tipo_mantenimiento": forms.Select(attrs={"class": "form-select"}),
            "tipo_estado": forms.Select(attrs={"class": "form-select"}),
            "estado_registro": forms.Select(attrs={"class": "form-select"}),
            "prioridad": forms.Select(attrs={"class": "form-select"}),
            "responsable": forms.Select(attrs={"class": "form-select"}),
            "fecha_reporte": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "fecha_fin_estimada": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "fecha_fin_real": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "tiempo_empleado_horas": forms.NumberInput(attrs={"class": "form-control", "step": "0.25", "min": "0"}),
            "costo_estimado": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "costo_real": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }
        labels = {
            "tipo_mantenimiento": "Tipo de mantenimiento *",
            "tipo_estado": "Tipo de estado actual *",
            "fecha_reporte": "Fecha de reporte / detección *",
            "fecha_inicio": "Fecha inicio mantenimiento *",
            "fecha_fin_estimada": "Fecha fin estimada",
            "fecha_fin_real": "Fecha fin real",
            "tiempo_empleado_horas": "Tiempo empleado (horas)",
            "prioridad": "Prioridad / urgencia *",
            "responsable": "Responsable / Técnico *",
            "costo_estimado": "Costo estimado",
            "costo_real": "Costo real",
            "estado_registro": "Estado del registro *",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tipo_mantenimiento"].queryset = TipoMantenimiento.objects.filter(activo=True).order_by("nombre")
        self.fields["tipo_mantenimiento"].empty_label = "-- Selecciona un tipo --"

        self.fields["tipo_estado"].queryset = TipoEstado.objects.filter(activo=True)
        self.fields["tipo_estado"].empty_label = "-- Selecciona un estado --"

        self.fields["estado_registro"].empty_label = "-- Selecciona el estado --"
        self.fields["prioridad"].empty_label = "-- Selecciona la prioridad --"
        self.fields["responsable"].queryset = Usuario.objects.all().order_by("nombre_completo", "numero_documento")
        self.fields["responsable"].empty_label = "-- Selecciona un técnico --"
        self.fields["responsable"].label_from_instance = (
            lambda u: f"{u.nombre_completo} ({u.numero_documento})"
        )

        if self.instance.pk and self.instance.producto_id:
            p = self.instance.producto
            self.fields["producto_busqueda"].initial = f"[{p.codigo_sku}] {p.nombre}"

    # Métodos clean (mantengo la lógica que tenías)
    def clean_producto(self):
        producto = self.cleaned_data.get("producto")
        if not producto:
            raise ValidationError("El ítem/herramienta es obligatorio.")
        return producto

    def clean_tipo_mantenimiento(self):
        tipo = self.cleaned_data.get("tipo_mantenimiento")
        if not tipo:
            raise ValidationError("Debes seleccionar un tipo de mantenimiento.")
        return tipo

    def clean_tipo_estado(self):
        estado = self.cleaned_data.get("tipo_estado")
        if not estado:
            raise ValidationError("Debes seleccionar el estado del equipo.")
        return estado

    def clean_fecha_reporte(self):
        fecha = self.cleaned_data.get("fecha_reporte")
        if not fecha:
            raise ValidationError("La fecha de reporte es obligatoria.")
        from datetime import date
        if fecha > date.today():
            raise ValidationError("La fecha de reporte no puede ser en el futuro.")
        return fecha

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get("fecha_inicio")
        if not fecha_inicio:
            raise ValidationError("La fecha de inicio es obligatoria.")
        return fecha_inicio

    def clean_responsable(self):
        responsable = self.cleaned_data.get("responsable")
        if not responsable:
            raise ValidationError("Debes asignar un técnico responsable.")
        return responsable

    def clean(self):
        cleaned = super().clean()
        # Validaciones cruzadas (resumidas)
        fecha_reporte = cleaned.get("fecha_reporte")
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_fin_estimada = cleaned.get("fecha_fin_estimada")
        fecha_fin_real = cleaned.get("fecha_fin_real")

        if fecha_reporte and fecha_inicio and fecha_inicio < fecha_reporte:
            self.add_error("fecha_inicio", "La fecha de inicio no puede ser anterior a la de reporte.")

        if fecha_inicio and fecha_fin_estimada and fecha_fin_estimada < fecha_inicio:
            self.add_error("fecha_fin_estimada", "La fecha estimada no puede ser anterior a la de inicio.")

        return cleaned


# ==================== MANTENIMIENTO UPDATE ====================

class MantenimientoUpdateForm(MantenimientoForm):
    MOTIVOS = MOTIVO_CAMBIO_CHOICES
    CAMPOS_TECNICO_EDITABLES = {"tiempo_empleado_horas"}

    motivo_edicion = forms.ChoiceField(
        label="Motivo de edición",
        choices=MOTIVOS,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    detalle_motivo = forms.CharField(
        label="Detalle del motivo (opcional)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    confirmar_cambios = forms.BooleanField(
        label="Confirmo que revisé los cambios antes de guardar",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, **kwargs):
        self.rol_usuario = (kwargs.pop("rol_usuario", "") or "").strip().lower()
        self.usuario_documento = kwargs.pop("usuario_documento", "")
        super().__init__(*args, **kwargs)

        if "tecnico" in self.rol_usuario:
            for field_name, field in self.fields.items():
                if field_name not in {"motivo_edicion", "detalle_motivo", "confirmar_cambios"}:
                    if field_name not in self.CAMPOS_TECNICO_EDITABLES:
                        field.disabled = True

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("confirmar_cambios"):
            self.add_error("confirmar_cambios", "Debes confirmar los cambios.")
        return cleaned


# ==================== DETALLE MANTENIMIENTO ====================

class DetalleMantenimientoForm(forms.ModelForm):

    class Meta:
        model = DetalleMantenimiento
        fields = ["tipo_mantenimiento", "tipo", "descripcion", "evidencia_adicional"]
        widgets = {
            "tipo_mantenimiento": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "evidencia_adicional": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        mantenimiento = kwargs.pop("mantenimiento", None)
        super().__init__(*args, **kwargs)

        self.fields["tipo_mantenimiento"].queryset = TipoMantenimiento.objects.filter(activo=True).order_by("nombre")
        self.fields["tipo_mantenimiento"].empty_label = "-- Selecciona un tipo --"
        self.fields["tipo"].empty_label = "-- Selecciona una entrada --"

        if mantenimiento and mantenimiento.tipo_mantenimiento_id:
            self.fields["tipo_mantenimiento"].initial = mantenimiento.tipo_mantenimiento

    def clean_descripcion(self):
        desc = self.cleaned_data.get("descripcion")
        if not desc or len(desc.strip()) < 10:
            raise ValidationError("La descripción es obligatoria y debe tener al menos 10 caracteres.")
        return desc