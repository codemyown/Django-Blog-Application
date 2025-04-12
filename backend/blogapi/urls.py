from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
