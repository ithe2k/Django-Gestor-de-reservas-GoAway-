from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("rosetta/", include("rosetta.urls")),
]


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("users/", include("users.urls")),
    path("propieties/", include("propieties.urls")),
    path("reservations/", include("reservations.urls")),
    prefix_default_language=True,
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
