import logging

from django_unicorn.components import UnicornView

from medux.settings import Scope
from medux.settings.models import ScopedSettings

logger = logging.getLogger(__file__)


class BaseNullableSwitchButton(UnicornView):
    template_name = "unicorn/core/nullable_switch_button.html"
    readonly = False
    _nullable: bool = True
    state: bool | None = None
    title = ""

    def set(self, state: bool | None) -> None:
        if self.readonly:
            return
        if state is None and not self._nullable:
            return
        self.state = state

    def clear(self) -> None:
        self.set(None)


class NullableSwitchButtonView(BaseNullableSwitchButton):
    namespace = ""
    settings_key = ""
    scope: Scope = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "scope" in kwargs:
            scope = kwargs["scope"]
            self.scope = Scope[scope]

    def mount(self):
        if not self.namespace:
            # FIXME: Unicorn needs to fix this bug:
            #  https://github.com/adamghill/django-unicorn/issues/380
            #  before raising Exceptions...

            # raise AttributeError( "NullableCheckbutton component needs
            # to have a 'namespace' attribute" )
            logger.critical(
                "ERROR: NullableCheckbutton component needs to have a 'namespace' attribute!"
            )
        if not self.settings_key:
            logger.critical(
                "ERROR: NullableCheckbutton component needs to have a 'settings_key' attribute!"
            )
        if not self.scope:
            logger.critical(
                "ERROR: NullableCheckbutton component needs to have a 'scope' attribute!"
            )
        self.state = ScopedSettings.get(self.namespace, self.settings_key, self.scope)

    def updating_state(self, value):
        print(value)
