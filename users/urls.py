from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user_list"),
    path("profile/", views.UserDetailView.as_view(), name="user_detail"),
    path("nuevo/", views.UserCreateView.as_view(), name="user_create"),
    path("profile/edit/", views.UserUpdateView.as_view(), name="user_update"),
    path("profile/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
