# Generated by Django 5.1 on 2024-10-22 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0008_remove_inmuebles_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmuebles',
            name='documentos',
            field=models.CharField(default='si', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inmuebles',
            name='observaciones',
            field=models.TextField(default='si'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inmuebles',
            name='planta',
            field=models.CharField(default='si', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inmuebles',
            name='pozo',
            field=models.CharField(default='si', max_length=255),
            preserve_default=False,
        ),
    ]
