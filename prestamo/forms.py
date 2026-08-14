from django import forms
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    """Formulario para crear/editar un préstamo."""

    class Meta:
        model = Prestamo
        fields = ['documento', 'observaciones', 'fecha', 'estado']
        labels = {
            'documento': 'Usuario responsable',
            'observaciones': 'Observaciones',
            'fecha': 'Fecha de préstamo',
            'estado': 'Estado',
        }
        widgets = {
            'documento': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }