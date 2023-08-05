from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from gdaps.pluginmanager import PluginManager

from .api.interfaces import IDashboardURL
from .views import DashboardView

app_name = "core"


# dynamically add all urlpatterns for the Dashboard that are provided by
# GDAPS plugins
dashboard_urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
]
PluginManager.load_plugin_submodule("urls")
for up in IDashboardURL:
    dashboard_urlpatterns += up.urlpatterns

root_urlpatterns = [
    path(
        "dashboard/",
        include((dashboard_urlpatterns, "dashboard"), namespace="dashboard"),
        name="index",
    ),
]


# URLs that should be part of all plugins and can be imported there.
common_urlpatterns = [
    path("unicorn/", include("django_unicorn.urls")),
    path(
        "accounts/login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
]
