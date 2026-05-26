import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from propieties.models import Propiedad


class Reservation(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pendiente de Pago")
        CONFIRMED = "CONFIRMED", _("Confirmada")
        CANCELED = "CANCELED", _("Cancelada")
        COMPLETED = "COMPLETED", _("Completada")

    huesped = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reservations",
        verbose_name=_("Huésped"),
    )
    propiedad = models.ForeignKey(
        Propiedad,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("Propiedad"),
    )

    # FECHAS
    check_in = models.DateField(_("Fecha de entrada"))
    check_out = models.DateField(_("Fecha de salida"))

    # CONTABILIDAD Y PRECIOS
    precio_por_noche = models.DecimalField(
        _("Precio por noche (€)"), max_digits=8, decimal_places=2
    )
    precio_total = models.DecimalField(
        _("Precio total (€)"),
        max_digits=10,
        decimal_places=2,
        editable=False,
    )

    # DATOS EXTRA Y LOGÍSTICA
    huespedes_totales = models.PositiveIntegerField(_("Número de huéspedes"))
    status = models.CharField(
        _("Estado de la reserva"),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    # AUDITORÍA
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
        ordering = ["-check_in"]

    def __str__(self):
        return f"Reserva {self.id} - {self.propiedad.titulo} por {self.huesped.email}"

    def clean(self):
        super().clean()

        # 1. Control de fechas lógicas (Salida posterior a la entrada)
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError({
                    "check_out": _(
                        "La fecha de salida debe ser posterior a la fecha de entrada."
                    )
                })

        if self.propiedad and self.huespedes_totales:
            if self.huespedes_totales > self.propiedad.capacidad_maxima:
                raise ValidationError({
                    "huespedes_totales": _(
                        f"El número de huéspedes excede la capacidad máxima de la propiedad ({self.propiedad.capacidad_maxima})."
                    )
                })

        if self.propiedad and self.check_in and self.check_out:
            # Buscamos reservas activas de esta propiedad (ignorando las canceladas)
            queryset = Reservation.objects.filter(propiedad=self.propiedad).exclude(
                status="CANCELED"
            )

            if self.id:
                queryset = queryset.exclude(id=self.id)

            # Validamos el colchón de 1 día contra el histórico activo
            for existing_res in queryset:
                limite_salida_con_limpieza = (
                    existing_res.check_out + datetime.timedelta(days=1)
                )
                limite_entrada_con_limpieza = (
                    existing_res.check_in - datetime.timedelta(days=1)
                )

                if (
                    self.check_in <= limite_salida_con_limpieza
                    and self.check_out >= limite_entrada_con_limpieza
                ):
                    raise ValidationError({
                        "check_in": _(
                            f"Las fechas solicitadas no están disponibles o entran en conflicto con el día "
                            f"de limpieza obligatorio de otra reserva activa ({existing_res.check_in} al {existing_res.check_out})."
                        )
                    })

    def save(self, *args, **kwargs):
        self.full_clean()

        noches = (self.check_out - self.check_in).days

        if not self.precio_por_noche:
            self.precio_por_noche = self.propiedad.precio_por_noche

        self.precio_total = self.precio_por_noche * noches

        super().save(*args, **kwargs)


class Payment(models.Model):
    METODOS_PAGO = [
        ("CARD", "Tarjeta de Crédito"),
        ("PAYPAL", "PayPal"),
        ("BIZUM", "Bizum"),
    ]

    reserva = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="pagos",
        verbose_name="Reserva",
    )
    cantidad = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Cantidad Pagada"
    )
    fecha_pago = models.DateTimeField(default=now, verbose_name="Fecha y Hora del Pago")
    metodo = models.CharField(
        max_length=10, choices=METODOS_PAGO, verbose_name="Método de Pago"
    )
    transaccion_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="ID de Transacción"
    )

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["-fecha_pago"]

    def __str__(self):
        return f"Pago de {self.cantidad}€ para Reserva #{self.reserva.id} ({self.get_metodo_display()})"
