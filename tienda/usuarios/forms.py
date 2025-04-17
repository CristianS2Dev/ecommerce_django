from django import forms
from django.core.exceptions import ValidationError
from .models import *

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'telefono', 'genero', 'fecha_nacimiento', 'imagen_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_imagen_perfil(self):
        imagen = self.cleaned_data.get('imagen_perfil', None)
        if imagen:
             # Validar el formato del archivo
            formatos_permitidos = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
            if imagen.content_type not in formatos_permitidos:
                raise ValidationError(f"Formato no permitido: {imagen.content_type}. Solo se aceptan: {', '.join(formatos_permitidos)}.")

        return imagen