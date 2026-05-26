from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Propiedad(models.Model):
    anfitrion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="propiedades",
        verbose_name=_("Anfitrión"),
        null=True,
        blank=False,
    )

    titulo = models.CharField(max_length=200, verbose_name=_("Título de la propiedad"))
    descripcion = models.TextField(verbose_name=_("Descripción"), blank=True, null=True)

    ciudad = models.CharField(max_length=100, verbose_name=_("Ciudad"))
    direccion = models.CharField(max_length=255, verbose_name=_("Dirección"))

    tamano = models.PositiveIntegerField(
        verbose_name=_("Tamaño (m²)"),
        help_text=_("Superficie útil en metros cuadrados"),
    )
    capacidad_maxima = models.PositiveIntegerField(
        verbose_name=_("Capacidad máxima de huéspedes"), default=2
    )
    precio_por_noche = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_("Precio por noche (€)")
    )

    tiene_piscina = models.BooleanField(
        default=False, verbose_name=_("¿Tiene Piscina?")
    )
    tiene_jardin = models.BooleanField(default=False, verbose_name=_("¿Tiene Jardín?"))
    tiene_wifi = models.BooleanField(default=True, verbose_name=_("¿Tiene Wi-Fi?"))
    admite_mascotas = models.BooleanField(
        default=False, verbose_name=_("¿Admite Mascotas?")
    )
    tiene_aire_acondicionado = models.BooleanField(
        default=False, verbose_name=_("¿Tiene Aire Acondicionado?")
    )

    imagen_principal = models.ImageField(
        upload_to="propiedades/principales/",
        blank=True,
        null=True,
        verbose_name=_("Imagen principal"),
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(
        default=True, verbose_name=_("Disponible para reservar")
    )

    class Meta:
        verbose_name = _("Propiedad")
        verbose_name_plural = _("Propiedades")
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.titulo} ({self.ciudad})"


def ruta_imagenes_propiedad(instance, filename):

    return f"propiedades/{instance.propiedad.id}/{filename}"


class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(
        Propiedad,
        related_name="imagenes",
        on_delete=models.CASCADE,
    )
    imagen = models.ImageField(upload_to=ruta_imagenes_propiedad)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Propiedad"
        verbose_name_plural = "Imágenes de Propiedads"

    def __str__(self):
        return f"Imagen {self.id} - Propiedad {self.propiedad.id}"
