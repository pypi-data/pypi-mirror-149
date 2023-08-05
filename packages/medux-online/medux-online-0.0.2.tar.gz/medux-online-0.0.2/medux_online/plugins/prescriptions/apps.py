from django.utils.translation import gettext_lazy as _

from medux.common.api import MeduxPluginAppConfig
from medux.settings import Scope, KeyType
from medux.settings.registry import SettingsRegistry
from . import __version__


class PrescriptionsConfig(MeduxPluginAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "medux_online.plugins.prescriptions"
    default = True  # FIXME: Remove when django bug is fixed

    groups_permissions = {
        "Prescription editors": {
            "prescriptions.PrescriptionRequest": ["view", "add", "change", "delete"],
        }
    }

    class PluginMeta:
        """This configuration is the introspection data for plugins."""

        # the plugin machine "name" is taken from the AppConfig,
        # so no name here
        verbose_name = _("Prescriptions")
        author = "Christian González"
        author_email = "office@nerdocs.at"
        vendor = "Nerdocs"
        description = _("Online prescriptions management.")
        category = _("Base")
        visible = True
        version = __version__
        # compatibility = "medux_online.core>=2.3.0"

    def ready(self):
        SettingsRegistry.register(
            "prescriptions",
            "medication_message",
            [Scope.TENANT],
            KeyType.STRING,
        )
        SettingsRegistry.register(
            "prescriptions",
            "show_medication_message",
            [Scope.TENANT],
            KeyType.BOOLEAN,
        )
        SettingsRegistry.register(
            "prescriptions",
            "update_requests_view_automatically",
            [Scope.TENANT],
            KeyType.BOOLEAN,
        )
        SettingsRegistry.register(
            "prescriptions",
            "use_approval",
            [Scope.TENANT],
            KeyType.BOOLEAN,
        )
