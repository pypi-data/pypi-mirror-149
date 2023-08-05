from django.utils.translation import gettext_lazy as _

from medux.common.api import MeduxPluginAppConfig
from . import __version__

default_app_config = "medux_online.plugins.homepage.apps.HomepageConfig"


class HomepageConfig(MeduxPluginAppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "medux_online.plugins.homepage"
    default = True  # FIXME: Remove when django bug is fixed

    groups_permissions = {
        "Site editors": {
            "homepage.HomepageSite": ["view", "change"],
        },
        "Homepage editors": {
            "homepage.TeamMember": ["view", "add", "change", "delete"],
            "homepage.Team": ["view", "add", "change", "delete"],
            "homepage.OpeningHourSlot": ["view", "add", "change", "delete"],
            "homepage.OpeningHours": ["view", "add", "change", "delete"],
            "homepage.News": ["view", "add", "change", "delete"],
            "homepage.Image": ["view", "add", "change", "delete"],
            "homepage.Gallery": ["view", "add", "change", "delete"],
            "homepage.Footer": ["view", "add", "change", "delete"],
            "homepage.Block": ["view", "add", "change", "delete"],
        },
    }

    class PluginMeta:
        """This configuration is the introspection data for plugins."""

        # the plugin machine "name" is taken from the AppConfig, so no name here
        verbose_name = _("Homepage")
        author = "Christian González"
        author_email = "office@nerdocs.at"
        vendor = "Nerdocs"
        description = _("The homepage plugin.")
        category = _("Base")
        visible = True
        version = __version__
        # compatibility = "medux_online.core>=2.3.0"
