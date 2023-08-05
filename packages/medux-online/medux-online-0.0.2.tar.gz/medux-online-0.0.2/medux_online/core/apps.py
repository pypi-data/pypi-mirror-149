from django.utils.translation import gettext_lazy as _

from medux.common.api import MeduxPluginAppConfig
from . import __version__


class CoreConfig(MeduxPluginAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "medux_online.core"
    default = True  # FIXME: Remove when django bug is fixed
    groups_permissions = {
        "Site editors": {
            "core.TermsAndConditionsPage": ["view", "add", "change", "delete"],
            "core.PrivacyPage": ["view", "add", "change", "delete"],
            "core.ClientManagementSite": ["view", "change"],
        },
        "Site admins": {
            "core.ClientManagementSite": ["add", "delete"],
        },
    }

    class PluginMeta:
        """This configuration is the introspection data for plugins."""

        # the plugin machine "name" is taken from the AppConfig, so no
        # name here
        verbose_name = _("Prescriptions")
        author = "Christian González"
        author_email = "office@nerdocs.at"
        vendor = "Nerdocs"
        description = _("MedUX Online - Core package")
        category = _("Base")
        visible = True
        version = __version__
        # compatibility = "medux_online.core>=2.3.0"
