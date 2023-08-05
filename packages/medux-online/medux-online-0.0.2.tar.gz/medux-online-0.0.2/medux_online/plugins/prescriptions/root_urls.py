from django.urls import path
from django.views.generic import TemplateView

from medux_online.core.urls import common_urlpatterns
from medux_online.core.views import PrivacyView, TermsView
from medux_online.plugins.prescriptions import views

# If the current site is a PrescriptionSite, this is the
# root URLCONF for prescriptions subdomains.

urlpatterns = common_urlpatterns + [
    path(
        "",
        views.CreatePrescriptionRequestView.as_view(),
        name="add",
    ),
    path(
        "thanks",
        TemplateView.as_view(template_name="prescriptions/thanks.html"),
        name="thanks",
    ),
    path("terms", TermsView.as_view(), name="terms"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
]

# path(
#     "<pk>/delete",
#     views.DeletePrescriptionRequestView.as_view(),
#     name="delete",
# ),
# path(
#     "<pk>",
#     views.PrescriptionRequestDetail.as_view(),
#     name="detail",
# ),
