

import django.db.models.deletion
from django.db import migrations, models

import propieties.models


class Migration(migrations.Migration):
    dependencies = [
        ("propieties", "0002_propiedad_anfitrion"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImagenPropiedad",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "imagen",
                    models.ImageField(
                        upload_to=propieties.models.ruta_imagenes_propiedad
                    ),
                ),
                ("fecha_subida", models.DateTimeField(auto_now_add=True)),
                (
                    "propiedad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="imagenes",
                        to="propieties.propiedad",
                    ),
                ),
            ],
            options={
                "verbose_name": "Imagen de Propiedad",
                "verbose_name_plural": "Imágenes de Propiedades",
            },
        ),
    ]
