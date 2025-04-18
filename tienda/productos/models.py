from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

# --- Categorías y Etiquetas ---

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# --- Marca ---

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='marcas/logos', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_original = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)]
    )
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    sku = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    en_oferta = models.BooleanField(default=False)

    def clean(self):
        """Valida los campos del producto."""
        if self.precio_original is not None and self.precio_original < 0:
            raise ValidationError("El precio original no puede ser negativo.")
        if self.descuento < 0:
            raise ValidationError("El descuento no puede ser negativo.")
        if self.descuento > 100:
            raise ValidationError("El descuento no puede ser mayor al 100%.")
        if self.precio_original is not None and self.en_oferta:
            precio_final = self.precio_original - (self.precio_original * self.descuento / Decimal(100))
            if precio_final < 0:
                raise ValidationError("El precio final no puede ser negativo.")

    @property
    def precio(self):
        """Calcula el precio final del producto."""
        if self.en_oferta and self.precio_original is not None and self.descuento > 0:
            return round(self.precio_original - (self.precio_original * self.descuento / Decimal(100)), 2)
        return self.precio_original

    @property
    def stock(self):
        """Calcula el stock total sumando el stock de todas las variantes."""
        return sum(variante.stock for variante in self.variantes.all())

    def save(self, *args, **kwargs):
        """Guarda el producto después de validarlo."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - ({self.stock} unidades)"

class Variante(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,related_name='variantes'
    )
    color = models.CharField(max_length=50)
    talla = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.producto.nombre} - {self.color} - {self.talla}"

# --- ImagenProducto (DEJADO COMO LO TIENES TÚ) ---

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

# --- Atributos personalizados (Material, Origen, etc.) ---

class AtributoProducto(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,related_name='atributos'
    )
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre}: {self.valor}"

    