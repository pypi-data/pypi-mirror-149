from django.urls import path

from .views.common import EditorView, HomepageView
from ...core.api.interfaces import IDashboardURL
from ...core.components.preferences import PreferencesView
from ...core.views import PrivacyView, TermsView

app_name = "homepage"

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    path("terms", TermsView.as_view(), name="terms"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
]


class HomepageDashboardURLs(IDashboardURL):
    urlpatterns = [
        path("preferences", PreferencesView.as_view(), name="preferences"),
        path("editor", EditorView.as_view(), name="homepage_editor"),
    ]
