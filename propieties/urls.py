
from django.urls import path

from . import views

app_name = "propieties"

urlpatterns = [
    path("dashboard/", views.AnfitrionDashboardView.as_view(), name="dashboard"),
    path("<int:pk>/", views.PropiedadDetailView.as_view(), name="detail"),
    path("nueva/", views.PropiedadCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", views.PropiedadUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", views.PropiedadDeleteView.as_view(), name="delete"),
    path(
        "search/", views.PropiedadSearchResultsListView.as_view(), name="search_results"
    ),
]
