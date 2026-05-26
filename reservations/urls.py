from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("", views.ReservationsListView.as_view(), name="reservations_list"),
    path("<int:pk>/create/", views.ReservationCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/editar/",
        views.ReservationUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/eliminar/",
        views.ReservationDeleteView.as_view(),
        name="delete",
    ),
    path("<int:pk>/pagar/", views.ReservationPaymentView.as_view(), name="payment"),
]
