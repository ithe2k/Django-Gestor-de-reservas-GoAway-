from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForms

from .models import User


class CustomUserCreationForm(DjangoUserCreationForms):
    class Meta(DjangoUserCreationForms.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "document_number",
            "phone_number",
            "role",
            "country",
        )


class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "document_number",
            "role",
            "country",
        )
