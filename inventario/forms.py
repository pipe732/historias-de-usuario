from django import forms
from .models import Herramienta, CategoriaHerramienta, Proveedor, Traslado
from almacenamiento.models import Existencia


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nit_proveedor", "telefono_contacto", "correo_proveedor", "descripcion"]
        widgets = {
            "nit_proveedor": forms.TextInput(attrs={"class": "form-control", "placeholder": "NIT"}),
            "telefono_contacto": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            "correo_proveedor": forms.TextInput(attrs={"class": "form-control", "placeholder": "correo@proveedor.com"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Existencia
        fields = ["num_estante", "cantidad", "responsable", "observaciones"]
        widgets = {
            "num_estante": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "responsable": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class MovimientosForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ["cantidad_total", "tipo_movimiento", "fecha_movimiento", "observaciones"]
        widgets = {
            "cantidad_total": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "tipo_movimiento": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_movimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaHerramienta
        fields = ["nombre_categoria", "tipo_herramienta", "descripcion"]
        widgets = {
            "nombre_categoria": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la categoría"}
            ),
            "tipo_herramienta": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tipo de herramienta"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción (opcional)"}
            ),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ["codigo_SKU", "nombre_herramienta", "descripcion", "disponibilidad", "fecha_ingreso", "codigo_categoria"]
        widgets = {
            "codigo_SKU": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: SKU-001"}),
            "nombre_herramienta": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de herramienta"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "disponibilidad": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_ingreso": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "codigo_categoria": forms.Select(attrs={"class": "form-select"}),
        }


class FiltroInventarioForm(forms.Form):
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar por nombre o SKU...",
            }
        ),
    )
    categoria = forms.ModelChoiceField(
        queryset=CategoriaHerramienta.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={"class": "form-select"}),
    )