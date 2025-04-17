
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    GENERO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('D', 'Doble Espiritu'),
        ('O', 'Otro'),
        ('N', 'No especificado')
    )
    genero = models.CharField(max_length=1, choices=GENERO, default='N')
    ROLES = (
        (1, "Administrador"),
        (2, "Cliente"),
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    imagen_perfil = models.ImageField(upload_to='usuarios/', null=True, blank=True)  # Campo para la foto de perfil

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """Guarda el usuario y maneja la imagen de perfil."""
        if self.pk:
            old_instance = Usuario.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.imagen_perfil and old_instance.imagen_perfil != self.imagen_perfil:
                old_image_path = os.path.join(settings.MEDIA_ROOT, old_instance.imagen_perfil.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)


        if not self.contrasena.startswith('pbkdf2_'):  # Evitar encriptar una contraseña ya encriptada
            self.contrasena = make_password(self.contrasena)

        super().save(*args, **kwargs)


class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100, default="Colombia")
    principal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Guarda la dirección y asegura que solo una dirección sea principal por usuario."""
        if self.principal:
            Direccion.objects.filter(usuario=self.usuario, principal=True).exclude(id=self.id).update(principal=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}, {self.estado}, {self.pais}"
