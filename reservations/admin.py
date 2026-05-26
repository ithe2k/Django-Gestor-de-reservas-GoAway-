from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "huesped",
        "propiedad",
        "check_in",
        "check_out",
        "precio_total",
        "status",
    )

    list_filter = ("status", "check_in", "check_out", "propiedad__ciudad")

    search_fields = (
        "huesped__email",
        "propiedad__titulo",
        "huesped__first_name",
        "huesped__last_name",
    )

    readonly_fields = ("precio_total", "created_at", "updated_at")

    fieldsets = (
        (
            _("Información del Huésped"),
            {"fields": ("huesped",)},
        ),
        (
            _("Información de la Propiedad"),
            {"fields": ("propiedad",)},
        ),
        (
            _("Fechas de la Reservación"),
            {"fields": ("check_in", "check_out")},
        ),
        (
            _("Precios"),
            {"fields": ("precio_por_noche", "precio_total")},
        ),
        (
            _("Detalles"),
            {"fields": ("huespedes_totales", "status")},
        ),
    )
