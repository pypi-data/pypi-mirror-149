from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from gdaps.pluginmanager import PluginManager

from medux_online.core.urls import common_urlpatterns

# this is the main URLconf file. It defines common used URLs for all hosts and collects all plugins' URLs.
urlpatterns = (
    PluginManager.urlpatterns()
    + common_urlpatterns
    + [
        path("admin/", admin.site.urls, name="admin"),
    ]
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
