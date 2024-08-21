from django.db import models
from hk_back.users.models import User

# Create your models here.
class Inmuebles(models.Model):
    TIPO_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
    ]

    ESTADOS_CHOICES = [
        ('disponible', 'Disponible'),
        ('no disponible', 'No disponible'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    asesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inmuebles')
    codigo = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES, default='venta')
    status = models.CharField(max_length=255, choices=ESTADOS_CHOICES, default='disponible')
