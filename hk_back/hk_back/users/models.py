from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('asesor', 'Asesor'),
    ]

    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='asesor')
    updated_at = models.DateTimeField(auto_now=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()