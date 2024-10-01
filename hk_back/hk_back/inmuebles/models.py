from django.db import models
from hk_back.users.models import User

# Create your models here.
class Inmuebles(models.Model):
    TIPO_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
    ]

    DISPONIBILIDAD_CHOICES = [
        ('disponible', 'Disponible'),
        ('no disponible', 'No disponible'),
    ]

    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    asesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inmuebles')
    codigo = models.CharField(max_length=255, unique=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    n_banos = models.CharField(max_length=255)
    n_habitaciones = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES, default='venta')
    disponibilidad = models.CharField(max_length=255, choices=DISPONIBILIDAD_CHOICES, default='disponible')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='activo')
