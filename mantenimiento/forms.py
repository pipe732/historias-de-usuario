from django import forms
from .models import DetalleMantenimiento, Mantenimiento


class TipoEstadoForm(forms.Form):
    pass


class TipoMantenimientoForm(forms.Form):
    pass


class MantenimientoUpdateForm(forms.Form):
    pass


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = [
            "codigo_herramienta",
            "tipo_mantenimiento",
            "fecha_ingreso",
            "fecha_salida",
            "observaciones",
        ]
        widgets = {
            "codigo_herramienta": forms.Select(attrs={"class": "form-select"}),
            "tipo_mantenimiento": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_ingreso": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "fecha_inicio": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "fecha_fin_real": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "observaciones": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class DetalleMantenimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMantenimiento
        fields = [
            "accion_realizada",
            "materiales_usados",
            "fecha_mantenimiento",
            "observacion",
        ]
        widgets = {
            "accion_realizada": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "materiales_usados": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "fecha_mantenimiento": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "observacion": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
        }
