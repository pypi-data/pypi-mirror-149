from django.urls import path

from medux_online.core.api.interfaces import IDashboardURL
from medux_online.plugins.prescriptions.components.prescriptionrequest_list import (
    PrescriptionrequestListView,
)

app_name = "prescriptions"


class PrescriptionDashboardURLs(IDashboardURL):
    urlpatterns = [
        path(
            # request admin view is listed under /dashboard/requests/
            "requests",
            PrescriptionrequestListView.as_view(),
            name="prescriptions-list",
        )
    ]
