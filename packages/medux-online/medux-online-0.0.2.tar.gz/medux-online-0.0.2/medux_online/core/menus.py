from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from menu import Menu

from medux.common.tools import MenuItem

user_menu = (
    MenuItem(
        _("Admin"),
        reverse_lazy("admin:index"),
        weight=80,
        icon="gear",
        separator=True,
        check=lambda request: request.user.is_superuser,
    ),
    MenuItem(
        _("Logout"),
        reverse_lazy("logout"),
        weight=90,
        icon="box-arrow-right",
        check=lambda request: request.user.is_authenticated,
    ),
)
Menu.add_item(
    "user",
    MenuItem(
        title=lambda request: request.user.username,
        url=None,
        weight=90,
        icon="person-fill",
        check=lambda request: request.user.is_authenticated,
        children=user_menu,
    ),
)

Menu.add_item(
    "user",
    MenuItem(
        _("Login"),
        reverse_lazy("login"),
        weight=90,
        icon="box-arrow-in-right",
        check=lambda request: request.user.is_anonymous,
    ),
)


# Menu.add_item(
#     "views",
#     MenuItem(
#         _("Preferences"),
#         reverse("preferences", host="core"),
#         weight=90,
#         icon="gear",
#         check=lambda request: request.user.is_authenticated,
#     ),
# )
Menu.add_item(
    "views",
    MenuItem(
        _("Editor"),
        reverse_lazy("dashboard:homepage_editor"),
        weight=50,
        icon="pencil-square",
        check=lambda request: request.user.is_authenticated,
    ),
)
