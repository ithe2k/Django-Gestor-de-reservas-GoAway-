import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from propieties.models import Propiedad

from .models import Payment, Reservation


class ReservationsListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservations/reservations_list.html"
    context_object_name = "reservations"
    paginate_by = 10

    def get_queryset(self):

        return Reservation.objects.filter(huesped=self.request.user).order_by(
            "-check_in"
        )


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = [
        "check_in",
        "check_out",
        "huespedes_totales",
        "is_recurrent",
        "frequency",
        "recurrence_count",
    ]
    template_name = "propieties/propieties_detail.html"
    context_object_name = "reservation"

    def get_success_url(self):
        return reverse("reservations:detail", kwargs={"pk": self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        propiedad_id = self.kwargs.get("pk") or self.kwargs.get("propiedad_id")
        propiedad_objeto = get_object_or_404(Propiedad, id=propiedad_id)

        if kwargs.get("instance") is None:
            kwargs["instance"] = Reservation()

        kwargs["instance"].propiedad = propiedad_objeto
        kwargs["instance"].huesped = self.request.user
        kwargs["instance"].precio_por_noche = propiedad_objeto.precio_por_noche

        if self.request.method == "GET" and not kwargs.get("data"):
            check_in_str = self.request.GET.get("check_in")
            check_out_str = self.request.GET.get("check_out")
            huespedes_str = self.request.GET.get("huespedes_totales")

            initial_data = {}
            if check_in_str:
                initial_data["check_in"] = check_in_str
            if check_out_str:
                initial_data["check_out"] = check_out_str
            if huespedes_str:
                initial_data["huespedes_totales"] = huespedes_str

            kwargs["initial"] = initial_data

        return kwargs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        propiedad_id = self.kwargs.get("pk") or self.kwargs.get("propiedad_id")
        context["propiedad"] = get_object_or_404(Propiedad, id=propiedad_id)

        context["search_check_in"] = self.request.GET.get("check_in")
        context["search_check_out"] = self.request.GET.get("check_out")
        context["search_huespedes"] = self.request.GET.get("huespedes_totales")

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            _("¡Reserva realizada correctamente! Tu estancia ha sido programada."),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Errores del formulario de reserva:", form.errors)
        messages.error(
            self.request,
            _("Hubo un error al procesar tu reserva. Revisa las fechas elegidas."),
        )
        return self.render_to_response(self.get_context_data(form=form))


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "reservations/reservation_detail.html"
    context_object_name = "reservation"


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation

    fields = [
        "check_in",
        "check_out",
        "huespedes_totales",
        "is_recurrent",
        "frequency",
        "recurrence_count",
    ]
    template_name = "reservations/reservation_form.html"

    def get_success_url(self):
        messages.success(
            self.request, _("¡Tu reserva ha sido modificada correctamente!")
        )
        return reverse_lazy("reservations:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["edit_mode"] = self.request.GET.get("edit")
        return context

    def form_valid(self, form):
        nuevo_check_in = form.cleaned_data["check_in"]
        nuevo_checkout = form.cleaned_data["check_out"]
        propiedad = self.object.propiedad

        check_in_con_limpieza = nuevo_check_in - datetime.timedelta(days=1)
        check_out_con_limpieza = nuevo_checkout + datetime.timedelta(days=1)

        conflictos = (
            Reservation.objects
            .filter(
                propiedad=propiedad, status__in=["PENDING", "CONFIRMED", "COMPLETED"]
            )
            .exclude(id=self.object.id)
            .filter(
                check_in__lte=check_out_con_limpieza,
                check_out__gte=check_in_con_limpieza,
            )
        )

        if conflictos.exists():
            form.add_error(
                None,
                _(
                    "Lo sentimos, las nuevas fechas seleccionadas entran en conflicto con otra reserva activa o con los días de limpieza."
                ),
            )
            return self.form_invalid(form)

        return super().form_valid(form)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = reverse_lazy("users:user_detail")
    template_name = "reservations/reservation_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.warning(
            request,
            _("La reserva ha sido cancelada. Las fechas vuelven a estar disponibles."),
        )
        return super().delete(request, *args, **kwargs)


class ReservationPaymentView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "reservations/reservation_payment.html"
    context_object_name = "reservation"

    def post(self, request, *args, **kwargs):
        reserva = self.get_object_or_404()
        metodo_elegido = request.POST.get("metodo")

        if reserva.status == "CONFIRMED":
            messages.info(request, _("Esta reserva ya se encuentra pagada."))
            return redirect("reservations:detail", pk=reserva.id)

        if metodo_elegido in ["CARD", "PAYPAL", "BIZUM"]:
            Payment.objects.create(
                reserva=reserva,
                cantidad=reserva.precio_total,
                metodo=metodo_elegido,
                transaccion_id=f"SIM-{reserva.id}-{int(timezone.now().timestamp())}",
            )

            reserva.status = "CONFIRMED"
            reserva.save()

            messages.success(
                request,
                _(
                    f"¡Pago procesado con éxito mediante {metodo_elegido}! Tu reserva está confirmada."
                ),
            )
            return redirect("reservations:detail", pk=reserva.id)

        messages.error(request, "Método de pago no válido.")
        return redirect("reservations:payment", pk=reserva.id)

    def get_object_or_404(self):
        return get_object_or_404(
            Reservation, pk=self.kwargs.get("pk"), huesped=self.request.user
        )
