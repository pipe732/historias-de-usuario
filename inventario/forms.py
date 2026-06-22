from django import forms
from .models import Producto, Categoria
from .models import Producto, Categoria, Proveedor, Inventario, Movimientos, Detalle_Movimientos

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nit_proveedor", "telefono_contacto", "correo_proveedor", "descripcion"]
        widgets = {
            "nit_proveedor": forms.TextInput(attrs={"class": "form-control", "placeholder": "NIT"}),
            "telefono_contacto": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            "correo_proveedor": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@proveedor.com"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ["producto", "id_estante", "cantidad", "responsable", "observaciones"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-select"}),
            "id_estante": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "responsable": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class MovimientosForm(forms.ModelForm):
    class Meta:
        model = Movimientos
        fields = ["inventario", "proveedor", "cantidad", "tipo_de_movimiento"]
        widgets = {
            "inventario": forms.Select(attrs={"class": "form-select"}),
            "proveedor": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "tipo_de_movimiento": forms.Select(attrs={"class": "form-select"}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la categoría"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción (opcional)"}
            ),
        }
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["codigo_sku", "nombre", "descripcion", "stock", "categoria"]
        widgets = {
            "codigo_sku": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: SKU-001"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del producto"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción (opcional)"}
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}
            ),
            "categoria": forms.Select(
                attrs={"class": "form-select"}
            ),
        }
        labels = {
            "codigo_sku": "Código / SKU",
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "stock": "Stock / Cantidad",
            "categoria": "Categoría",
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
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={"class": "form-select"}),
    )