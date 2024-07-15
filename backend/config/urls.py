from config import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("book.urls")),
    path("", include("authentications.urls")),
    path("api/v1/", include("rating.urls")),
    path("api/v1/", include("reviews.urls")),
]


# urls для swagger
urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
