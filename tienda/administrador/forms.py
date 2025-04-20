from django import forms
from django.forms import inlineformset_factory
from tienda.productos.models import Variante, Producto


class VarianteForm(forms.ModelForm):
    class Meta:
        model = Variante
        fields = ['color', 'talla', 'stock']
        widgets = {
           'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'style': 'height: 38px; padding: 2px;'}),
            'talla': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_original', 'descuento', 'en_oferta', 'sku', 'categoria', 'marca', 'etiquetas']

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        qs = Producto.objects.filter(sku=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("El SKU ya está en uso por otro producto.")
        return sku


VarianteFormSet = inlineformset_factory(
    parent_model=Producto,
    model=Variante,
    form=VarianteForm,
    extra=0,
    can_delete=True,
    min_num=0,          # Permitir cero variantes
    validate_min=False  # No validar mínimo
)