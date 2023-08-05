from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from menu import Menu

from medux.common.tools import MenuItem
from .components.prescriptionrequest_list import get_prescriptionrequest_count

Menu.add_item(
    "views",
    MenuItem(
        _("Prescriptions list"),
        reverse_lazy("dashboard:prescriptions-list"),
        weight=30,
        icon="list-check",
        badge=get_prescriptionrequest_count,
        check=lambda request: request.user.has_perm("can view prescriptions"),
    ),
)
