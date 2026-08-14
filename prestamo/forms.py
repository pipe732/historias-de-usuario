# prestamo/forms.py
from django import forms
from django.utils import timezone
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    """Formulario para crear/editar un préstamo."""

    class Meta:
        model  = Prestamo
        fields = ['documento', 'nombre_usuario', 'observaciones', 'fecha_vencimiento']
        labels = {
            'documento':        'Documento / ID del usuario',
            'nombre_usuario':   'Nombre del usuario',
            'observaciones':    'Observaciones',
            'fecha_vencimiento': 'Fecha de vencimiento',
        }
        widgets = {
            'documento': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Documento o ID',
                'id':          'id_usuario',
                'readonly':    True,
            }),
            'nombre_usuario': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Nombre completo del responsable',
                'readonly':    True,
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Notas adicionales (opcional)...',
            }),
            'fecha_vencimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type':  'date',
                }
            ),
        }

    def clean_documento(self):
        documento = self.cleaned_data.get('documento', '').strip()
        if not documento:
            raise forms.ValidationError('El documento/ID del usuario no puede estar vacío.')
        if documento == '-1':
            raise forms.ValidationError('Usuario no válido.')
        return documento

    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get('documento')
        nombre_usuario = cleaned_data.get('nombre_usuario')
        if documento and nombre_usuario:
            from usuario.models import Usuario
            try:
                user = Usuario.objects.get(numero_documento=documento)
                if user.nombre_completo != nombre_usuario:
                    raise forms.ValidationError('El nombre del usuario no coincide con el documento.')
            except Usuario.DoesNotExist:
                raise forms.ValidationError('Usuario no encontrado.')
        return cleaned_data