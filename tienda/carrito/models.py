from django.db import models
from tienda.productos.models import Producto


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
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """Calcula el subtotal del elemento (precio del producto * cantidad)."""
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"