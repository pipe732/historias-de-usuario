from django import forms
from .models import Estante, Almacen
from inventario.models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku', 'nombre', 'descripcion', 'stock', 'categoria']
        widgets = {
            'codigo_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }



class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ['nombre', 'detalles', 'capacidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EstanteForm(forms.ModelForm):
    class Meta:
        model = Estante
        fields = ['almacen', 'codigo', 'detalles', 'capacidad']
        widgets = {
            'almacen': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }