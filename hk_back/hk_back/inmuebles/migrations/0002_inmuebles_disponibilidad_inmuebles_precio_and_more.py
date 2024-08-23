# Generated by Django 5.1 on 2024-08-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmuebles',
            name='disponibilidad',
            field=models.CharField(choices=[('disponible', 'Disponible'), ('no disponible', 'No disponible')], default='disponible', max_length=255),
        ),
        migrations.AddField(
            model_name='inmuebles',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inmuebles',
            name='status',
            field=models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=255),
        ),
    ]
