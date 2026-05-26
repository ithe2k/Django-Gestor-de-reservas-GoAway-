

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título de la propiedad')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('ciudad', models.CharField(max_length=100, verbose_name='Ciudad')),
                ('direccion', models.CharField(max_length=255, verbose_name='Dirección')),
                ('tamano', models.PositiveIntegerField(help_text='Superficie útil en metros cuadrados', verbose_name='Tamaño (m²)')),
                ('capacidad_maxima', models.PositiveIntegerField(default=2, verbose_name='Capacidad máxima de huéspedes')),
                ('precio_por_noche', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Precio por noche (€)')),
                ('tiene_piscina', models.BooleanField(default=False, verbose_name='¿Tiene Piscina?')),
                ('tiene_jardin', models.BooleanField(default=False, verbose_name='¿Tiene Jardín?')),
                ('tiene_wifi', models.BooleanField(default=True, verbose_name='¿Tiene Wi-Fi?')),
                ('admite_mascotas', models.BooleanField(default=False, verbose_name='¿Admite Mascotas?')),
                ('tiene_aire_acondicionado', models.BooleanField(default=False, verbose_name='¿Tiene Aire Acondicionado?')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True, verbose_name='Disponible para reservar')),
            ],
            options={
                'verbose_name': 'Propiedad',
                'verbose_name_plural': 'Propiedades',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
