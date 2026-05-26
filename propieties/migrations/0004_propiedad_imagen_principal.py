

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propieties', '0003_imagenpropiedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='propiedad',
            name='imagen_principal',
            field=models.ImageField(blank=True, null=True, upload_to='propiedades/principales/', verbose_name='Imagen principal'),
        ),
    ]
