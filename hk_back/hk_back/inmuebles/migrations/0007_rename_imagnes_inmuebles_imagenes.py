# Generated by Django 5.1 on 2024-10-09 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0006_inmuebles_imagnes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inmuebles',
            old_name='imagnes',
            new_name='imagenes',
        ),
    ]
