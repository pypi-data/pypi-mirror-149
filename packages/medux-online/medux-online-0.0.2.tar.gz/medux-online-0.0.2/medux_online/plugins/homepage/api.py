from django.forms import Form
from gdaps.api import Interface


@Interface
class ISettingsForm:
    """The Interface for Settings entries.

    Each entry has an icon, a title and a form and can be rendered by a Django template.
    """

    def icon(self) -> str:
        """:returns an bootstrap icon name that should be drawn for that settings part, like "gear"."""

    def title(self) -> str:
        """:returns a title for that settings part."""

    def form(self) -> Form:
        """:returns the form that should be included to the main settings page.

        The form fields must be in the format <app_name>__<settings_key> to be recognized,
        like

            homepage__my_settings_key = forms.CharField(...)

        Mind the double underscore between the app name and the key.
        The key is then available in templates under `settings.<app_name>.<key>`.
        """
