# Generated by Django 5.1.1 on 2025-04-17 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=100, null=True)),
                ('imagen', models.ImageField(upload_to='banners/')),
                ('tipo', models.CharField(choices=[('principal', 'Principal'), ('secundario', 'Secundario')], default='principal', max_length=50)),
            ],
        ),
    ]
