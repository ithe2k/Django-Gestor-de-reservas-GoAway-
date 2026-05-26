

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propieties', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='propiedad',
            name='anfitrion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='propiedades', to=settings.AUTH_USER_MODEL, verbose_name='Anfitrión'),
        ),
    ]
