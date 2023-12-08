import secret_info
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from WeddingWebsite.views import error_404

from django.conf import settings
from django.conf.urls.static import static

# custom 404 page
handler404 = error_404

urlpatterns = [
    path(secret_info.admin_url, admin.site.urls),
    path("", include("WeddingWebsite.urls")),
]

# allow Django to serve Media files if DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
