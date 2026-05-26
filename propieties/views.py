import datetime
from io import BytesIO

import cloudinary.uploader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from PIL import Image

from reservations.models import Reservation

from .forms import PropiedadForm
from .models import ImagenPropiedad, Propiedad


class AnfitrionDashboardView(LoginRequiredMixin, ListView):
    model = Propiedad
    template_name = "propieties/dashboard_anfitrion.html"
    context_object_name = "propiedades"

    def get_queryset(self):

        return Propiedad.objects.filter(anfitrion=self.request.user)


class PropiedadDetailView(LoginRequiredMixin, DetailView):
    model = Propiedad
    template_name = "propieties/propieties_detail.html"
    context_object_name = "propiedad"


class PropiedadCreateView(LoginRequiredMixin, CreateView):
    model = Propiedad
    form_class = PropiedadForm
    template_name = "propieties/propieties_forms.html"
    success_url = reverse_lazy("propieties:dashboard")

    def form_valid(self, form):
        form.instance.anfitrion = self.request.user
        self.object = form.save()
        self._procesar_imagenes(self.object)
        return redirect(self.get_success_url())

    def _procesar_imagenes(self, propiedad):
        """Procesa y guarda las imágenes de la propiedad"""
        imagenes = self.request.FILES.getlist("imagenes")

        if imagenes:
            for idx, img_file in enumerate(imagenes):
                try:
                    ImagenPropiedad.objects.create(
                        propiedad=propiedad,
                        imagen=img_file,
                    )

                    if idx == 0:
                        self._crear_miniatura(propiedad, img_file)
                except Exception as e:
                    print(f"Error guardando imagen {idx}: {str(e)}")

    def _crear_miniatura(self, propiedad, imagen_file):
        """Crea miniatura de la imagen para imagen_principal"""
        try:
            # Aseguramos que el puntero esté al inicio si viene de memoria
            if hasattr(imagen_file, "seek"):
                imagen_file.seek(0)

            img = Image.open(imagen_file)

            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img)
                img = background

            img.thumbnail((400, 300), Image.Resampling.LANCZOS)

            img_io = BytesIO()
            img.save(img_io, format="JPEG", quality=85)
            img_io.seek(0)

            filename = f"thumbnail_propiedad_{propiedad.id}.jpg"
            propiedad.imagen_principal.save(
                filename, ContentFile(img_io.read()), save=True
            )
        except Exception as e:
            print(f"Error creando miniatura: {str(e)}")
        finally:
            if hasattr(imagen_file, "seek"):
                imagen_file.seek(0)


class PropiedadUpdateView(LoginRequiredMixin, UpdateView):
    model = Propiedad
    template_name = "propieties/propieties_forms.html"
    form_class = PropiedadForm
    success_url = reverse_lazy("propieties:dashboard")

    def get_queryset(self):
        return Propiedad.objects.filter(anfitrion=self.request.user)

    def form_valid(self, form):
        self.object = form.save()

        # 🛠️ SECCIÓN CORREGIDA: Borrado adaptado a Cloudinary sin usar .path
        ids_a_eliminar = self.request.POST.getlist("eliminar_imagenes")
        if ids_a_eliminar:
            imagenes_a_borrar = ImagenPropiedad.objects.filter(
                propiedad=self.object, id__in=ids_a_eliminar
            )
            for img_obj in imagenes_a_borrar:
                if img_obj.imagen:
                    try:
                        # Cloudinary elimina usando el campo .name interno del objeto
                        cloudinary.uploader.destroy(img_obj.imagen.name)
                    except Exception as e:
                        print(f"Error borrando imagen de Cloudinary: {str(e)}")

                img_obj.delete()

        self._procesar_imagenes(self.object)

        if not self.object.imagen_principal and self.object.imagenes.exists():
            primera_restante = self.object.imagenes.first()
            # 💡 IMPORTANTE: Si la imagen ya está en Cloudinary, pasamos el archivo abierto
            try:
                self._crear_miniatura(self.object, primera_restante.imagen.file)
            except Exception as e:
                print(f"No se pudo generar miniatura desde la nube: {str(e)}")

        return redirect(self.get_success_url())

    def _procesar_imagenes(self, propiedad):
        """Procesa y guarda nuevas imágenes de la propiedad"""
        imagenes = self.request.FILES.getlist("imagenes")

        if imagenes:
            primera = True
            for img_file in imagenes:
                try:
                    ImagenPropiedad.objects.create(
                        propiedad=propiedad,
                        imagen=img_file,
                    )

                    if primera:
                        self._crear_miniatura(propiedad, img_file)
                        primera = False
                except Exception as e:
                    print(f"Error guardando imagen: {str(e)}")

    def _crear_miniatura(self, propiedad, imagen_file):
        """Crea miniatura de la imagen para imagen_principal"""
        try:
            if hasattr(imagen_file, "seek"):
                imagen_file.seek(0)

            img = Image.open(imagen_file)

            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img)
                img = background

            img.thumbnail((400, 300), Image.Resampling.LANCZOS)

            img_io = BytesIO()
            img.save(img_io, format="JPEG", quality=85)
            img_io.seek(0)

            filename = f"thumbnail_propiedad_{propiedad.id}.jpg"
            propiedad.imagen_principal.save(
                filename, ContentFile(img_io.read()), save=True
            )
        except Exception as e:
            print(f"Error creando miniatura: {str(e)}")
        finally:
            if hasattr(imagen_file, "seek"):
                imagen_file.seek(0)


class PropiedadDeleteView(LoginRequiredMixin, DeleteView):
    model = Propiedad
    template_name = "propieties/propieties_confirm_delete.html"
    success_url = reverse_lazy("propieties:dashboard")

    def get_queryset(self):

        return Propiedad.objects.filter(anfitrion=self.request.user)


class PropiedadSearchResultsListView(ListView):
    model = Propiedad
    template_name = "propieties/search_results.html"
    context_object_name = "properties"

    def get_queryset(self):

        location = self.request.GET.get("search")
        check_in_str = self.request.GET.get("checkin")
        check_out_str = self.request.GET.get("checkout")

        adults_str = self.request.GET.get("adults")
        kids_str = self.request.GET.get("kids")

        queryset = Propiedad.objects.all()

        if location:
            queryset = queryset.filter(ciudad__icontains=location)

        try:
            adults = int(adults_str) if adults_str else 0
            kids = int(kids_str) if kids_str else 0
            total_huespedes = adults + kids

            if total_huespedes > 0:
                queryset = queryset.filter(capacidad_maxima__gte=total_huespedes)
        except ValueError:
            pass

        if check_in_str and check_out_str:
            try:
                check_in = datetime.datetime.strptime(check_in_str, "%Y-%m-%d").date()
                check_out = datetime.datetime.strptime(check_out_str, "%Y-%m-%d").date()

                check_in_con_limpieza = check_in - datetime.timedelta(days=1)
                check_out_con_limpieza = check_out + datetime.timedelta(days=1)

                propiedades_ocupadas_ids = (
                    Reservation.objects
                    .filter(status__in=["PENDING", "CONFIRMED", "COMPLETED"])
                    .filter(
                        check_in__lte=check_out_con_limpieza,
                        check_out__gte=check_in_con_limpieza,
                    )
                    .values_list("propiedad_id", flat=True)
                )

                queryset = queryset.exclude(id__in=propiedades_ocupadas_ids)

            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            adults = int(self.request.GET.get("adults", 0) or 0)
            kids = int(self.request.GET.get("kids", 0) or 0)
            context["search_huespedes"] = adults + kids
        except ValueError:
            context["search_huespedes"] = self.request.GET.get("adults")

        context["search_check_in"] = self.request.GET.get("checkin")
        context["search_check_out"] = self.request.GET.get("checkout")
        return context
