from django import forms
from tienda.productos.models import Variante

class VarianteForm(forms.ModelForm):
    class Meta:
        model = Variante
        fields = ['color', 'talla', 'stock']
        widgets = {
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'talla': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }