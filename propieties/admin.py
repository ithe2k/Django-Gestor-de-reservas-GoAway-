from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ImagenPropiedad, Propiedad



class ImagenPropiedadInline(admin.TabularInline):
    model = ImagenPropiedad
    extra = 1
    fields = ("imagen", "fecha_subida")
    readonly_fields = ("fecha_subida",)


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "ciudad",
        "precio_por_noche",
        "capacidad_maxima",
        "activo",
        "tiene_piscina",
    )

    list_filter = ("ciudad", "activo", "tiene_piscina", "tiene_wifi", "admite_mascotas")

    search_fields = ("titulo", "descripcion", "ciudad")

    inlines = [ImagenPropiedadInline]


    fieldsets = (
        (
            _("Información General"),
            {
                "fields": (
                    "titulo",
                    "descripcion",
                    "precio_por_noche",
                    "activo",
                    "imagen_principal",
                )
            },
        ),
        (_("Ubicación"), {"fields": ("ciudad", "direccion")}),
        (_("Características y Capacidad"), {"fields": ("tamano", "capacidad_maxima")}),
        (
            _("Extras y Servicios (Marcar si dispone de ellos)"),
            {
                "classes": ("wide",),
                "fields": (
                    "tiene_piscina",
                    "tiene_jardin",
                    "tiene_wifi",
                    "admite_mascotas",
                    "tiene_aire_acondicionado",
                ),
            },
        ),
    )


@admin.register(ImagenPropiedad)
class ImagenPropiedadAdmin(admin.ModelAdmin):
    list_display = ("propiedad", "fecha_subida")
    list_filter = ("propiedad", "fecha_subida")
    search_fields = ("propiedad__titulo",)
