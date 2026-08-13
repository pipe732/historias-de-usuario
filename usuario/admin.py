from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display    = ('documento', 'primer_nombre', 'primer_apellido', 'correo_personal',
                       'tipo_documento', 'rol', 'telefono')
    list_filter     = ('rol', 'tipo_documento')
    search_fields   = ('documento', 'primer_nombre', 'primer_apellido', 'correo_personal')
    ordering        = ('primer_nombre', 'primer_apellido')
    readonly_fields = ('documento',)

    fieldsets = (
        ('Información personal', {
            'fields': ('documento', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_documento',
                       'correo_personal', 'telefono', 'programa', 'ficha'),
        }),
        ('Acceso', {
            'fields': ('rol', 'password'),
            'description': 'La contraseña se guarda cifrada automáticamente al guardar.',
        }),
        ('Relaciones', {
            'fields': ('destinado', 'solicitado'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            raw = form.cleaned_data['password']
            if not raw.startswith(('pbkdf2_', 'bcrypt', 'argon2')):
                obj.password = make_password(raw)
        super().save_model(request, obj, form, change)