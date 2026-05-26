

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cantidad Pagada')),
                ('fecha_pago', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha y Hora del Pago')),
                ('metodo', models.CharField(choices=[('CARD', 'Tarjeta de Crédito'), ('PAYPAL', 'PayPal'), ('BIZUM', 'Bizum')], max_length=10, verbose_name='Método de Pago')),
                ('transaccion_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID de Transacción')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='reservations.reservation', verbose_name='Reserva')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
                'ordering': ['-fecha_pago'],
            },
        ),
    ]
