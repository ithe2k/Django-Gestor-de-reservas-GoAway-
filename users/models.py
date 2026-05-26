from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("El correo electrónico es obligatorio."))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


""" use*_name, first_name, last_name, email, password, is_staff, is_active, date_joined, groups y user_permissions. """


class User(AbstractUser):
    email = models.EmailField(_("Dirección de correo electrónico"), unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
    document_number = models.CharField(
        _("DNI o Pasaporte"), max_length=20, unique=True, blank=True, null=True
    )

    phone_number = models.CharField(
        _("Teléfono"), max_length=9, unique=True, blank=True, null=True
    )

    country = CountryField(
        _("País"),
        blank=True,
        null=True,
        blank_label=_("— Selecciona un país —"),
    )

    class role(models.TextChoices):
        DEFAULT = "DEFAULT", _("-")
        HOST = "HOST", _("Anfitrion")
        GUEST = "GUEST", _("Huésped")

    role = models.CharField(
        _("Rol"),
        max_length=10,
        choices=role.choices,
        default=role.DEFAULT,
    )

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

    def __str__(self):
        return self.email
