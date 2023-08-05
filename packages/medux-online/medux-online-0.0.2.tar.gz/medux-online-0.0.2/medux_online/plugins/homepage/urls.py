from django.urls import path

from .views.common import EditorView
from ...core.api.interfaces import IDashboardURL
from ...core.components.preferences import PreferencesView

app_name = "homepage"


class HomepageDashboardURLs(IDashboardURL):
    urlpatterns = [
        path("preferences", PreferencesView.as_view(), name="preferences"),
        path("editor", EditorView.as_view(), name="homepage_editor"),
    ]
