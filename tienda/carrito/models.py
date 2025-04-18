from django.db import models
from tienda.productos.models import *


class Carrito(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, null=True, blank=True, related_name='carritos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def total(self):
        """Calcula el total del carrito sumando los subtotales de los elementos."""
        return sum(item.subtotal() for item in self.elementos.all()) if self.elementos.exists() else 0

    def __str__(self):
        return f"Carrito de {self.usuario.nombre if self.usuario else 'Invitado'}"


class ElementoCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante, on_delete=models.CASCADE, null=True, blank=True)  # Agrega este campo
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * (self.producto.precio if self.producto else 0)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"