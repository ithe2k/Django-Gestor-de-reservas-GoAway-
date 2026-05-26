from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import User




class OwnerOrStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        current_user = self.request.user
        obj_user = self.get_object()
        return current_user == obj_user or current_user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied


class OnlyStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied





class UserListView(LoginRequiredMixin, OnlyStaffRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("base:landing")
    success_message = _("El usuario ha sido creado correctamente")


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "profile_user"

    def get_object(self, queryset=None):

        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()


        context["my_bookings"] = user.reservations.all().order_by("-check_in")


        if user.role == "HOST" and hasattr(user, "propiedades"):
            context["my_properties"] = user.propiedades.all().order_by(
                "-fecha_creacion"
            )
        else:
            context["my_properties"] = None

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = (
        CustomUserUpdateForm
    )
    template_name = "users/user_forms.html"
    success_url = reverse_lazy(
        "users:user_detail"
    )
    success_message = _("El usuario ha sido actualizado correctamente")

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, OwnerOrStaffRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    context_object_name = "profile_user"
    success_url = reverse_lazy("base:landing")
    success_message = _("El usuario ha sido eliminado correctamente")

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):

        logout(request)
        return super().delete(request, *args, **kwargs)
