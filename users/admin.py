from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import User

add_form = CustomUserCreationForm
change_form = CustomUserUpdateForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = change_form
    add_form = add_form

    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active", "date_joined")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name", "document_number")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Información Personal"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "document_number",
                    "phone_number",
                    "country",
                )
            },
        ),
        (
            _("Permisos"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Fechas Importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "document_number",
                    "country",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
