

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('propieties', '0004_propiedad_imagen_principal'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField(verbose_name='Fecha de entrada')),
                ('check_out', models.DateField(verbose_name='Fecha de salida')),
                ('precio_por_noche', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Precio por noche (€)')),
                ('precio_total', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Precio total (€)')),
                ('huespedes_totales', models.PositiveIntegerField(verbose_name='Número de huéspedes')),
                ('status', models.CharField(choices=[('PENDING', 'Pendiente de Pago'), ('CONFIRMED', 'Confirmada'), ('CANCELED', 'Cancelada'), ('COMPLETED', 'Completada')], default='PENDING', max_length=20, verbose_name='Estado de la reserva')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('huesped', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to=settings.AUTH_USER_MODEL, verbose_name='Huésped')),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='propieties.propiedad', verbose_name='Propiedad')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['-check_in'],
            },
        ),
    ]
