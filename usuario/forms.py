from django import forms
from .models import Usuario, Rol


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'documento',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'correo_personal',
            'telefono',
            'tipo_documento',
            'programa',
            'ficha',
            'destinado',
            'solicitado',
        ]
        widgets = {
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1234567890'
            }),
            'primer_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primer nombre'
            }),
            'segundo_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo nombre (opcional)'
            }),
            'primer_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primer apellido'
            }),
            'segundo_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo apellido (opcional)'
            }),
            'correo_personal': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3001234567'
            }),
            'tipo_documento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'programa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Programa de formación'
            }),
            'ficha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de ficha'
            }),
            'destinado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'solicitado': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'documento': 'Número de Documento',
            'primer_nombre': 'Primer Nombre',
            'segundo_nombre': 'Segundo Nombre',
            'primer_apellido': 'Primer Apellido',
            'segundo_apellido': 'Segundo Apellido',
            'correo_personal': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'tipo_documento': 'Tipo de Documento',
            'programa': 'Programa',
            'ficha': 'Ficha',
            'destinado': 'Destinado a',
            'solicitado': 'Solicitado por',
        }

    def clean_documento(self):
        numero = str(self.cleaned_data.get('documento') or '').strip()
        if not numero.isdigit():
            raise forms.ValidationError('El número de documento solo debe contener dígitos.')
        return numero

    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono') or '').strip()
        if telefono and not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener dígitos.')
        return telefono

    def clean_correo_personal(self):
        correo = self.cleaned_data.get('correo_personal')
        if correo and Usuario.objects.filter(correo_personal=correo).exclude(documento=self.instance.documento).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return correo