# Generated by Django 5.1.1 on 2025-04-16 23:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='marcas/logos')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('precio_original', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('stock', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('en_oferta', models.BooleanField(default=False)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='tienda.categoria')),
                ('etiquetas', models.ManyToManyField(blank=True, to='tienda.etiqueta')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='tienda.marca')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='productos/')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='AtributoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=200)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atributos', to='tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Variante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('talla', models.CharField(max_length=50)),
                ('stock', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variantes', to='tienda.producto')),
            ],
        ),
    ]
