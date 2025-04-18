

from django.contrib import admin
from .models import Categoria, Etiqueta, Marca, Producto, Variante, ImagenProducto

admin.site.register(Categoria)
admin.site.register(Etiqueta)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Variante)
admin.site.register(ImagenProducto)

