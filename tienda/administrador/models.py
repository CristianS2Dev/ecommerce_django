
from django.db import models

class Banner(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.ImageField(upload_to='banners/')
    tipo = models.CharField(
        max_length=50,
        choices=(
            ('principal', 'Principal'),
            ('secundario', 'Secundario'),
        ),
        default='principal'
    )   

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"