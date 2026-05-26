from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from propieties.models import Propiedad

from .forms import LoginForm


def landing(request):

    ciudades_disponibles = (
        Propiedad.objects.values_list("ciudad", flat=True).distinct().order_by("ciudad")
    )

    context = {
        "ciudades": ciudades_disponibles,
    }
    return render(request, "base/landing.html", context)


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("base:landing")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("base:landing")
