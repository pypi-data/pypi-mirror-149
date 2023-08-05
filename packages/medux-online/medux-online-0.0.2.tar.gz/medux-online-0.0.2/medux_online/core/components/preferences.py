import logging
from typing import Tuple, Dict, Any

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _
from django_unicorn.components import UnicornView

from medux.settings import Scope, ScopeIcons, SettingsRegistry
from medux.settings.models import ScopedSettings

logger = logging.getLogger(__file__)


class PreferencesView(PermissionRequiredMixin, UnicornView):
    """Loads all settings and creates a form of them dynamically.

    The "object_list" property is a nested dict with the content
    namespace->key->scope->data, e.g.

    prescriptions
        show_medication
            TENANT
                field_name: "..."
                value: "..."
            VENDOR
                ...
    """

    template_name = "core/preferences.html"
    permission_required = ["can change scoped settings"]
    namespaces = None
    # [namespace][key][scope]
    object_list: Dict[str, Dict[str, Dict[str, str | Any]]] = {}

    active_tab = None

    class Meta:
        javascript_exclude = ["permission_required"]

    def __init__(self, *args, **kwargs):
        # get a list of settings and create dynamic Unicorn properties
        # from them
        for namespace, key, scope, key_type in SettingsRegistry.all():
            setattr(PreferencesView, f"{namespace}__{key}__{scope.name.lower()}", "")
            setattr(PreferencesView, f"{namespace}__{key}__effective", "")

        super().__init__(*args, **kwargs)

    def mount(self):
        from medux.settings.models import ScopedSettings

        # set active_tab to first one
        self.namespaces = ScopedSettings.namespaces()
        self.namespaces.sort()
        self.active_tab = self.namespaces[0]

        for namespace, key, scope, key_type in SettingsRegistry.all():
            filter = {
                "namespace": namespace,
                "key": key,
                "scope": scope,
            }
            if scope == Scope.USER:
                # user setting requested. Always take current user,
                # so users can just see their own user settings
                # FIXME: don't allow admins/non-tenant users
                #  to set own fields
                filter["user"] = self.request.user
            elif scope == Scope.TENANT:
                # if tenant setting is requested, user needs to have
                # access to that tenant's settings here the current
                # viewed homepage's tenant is meant, not user.tenant!
                filter["tenant"] = self.request.tenant
                # TODO: make sure that setting is r/o if user has no
                #  access to it.
            # elif scope == Scope.DEVICE:
            #     fk["device"] = self.request. ...
            instance = ScopedSettings.get(**filter, full_object=True)
            if not instance:
                # first-time create empty settings at read access
                instance = ScopedSettings.objects.create(**filter)
                instance.save()
            field_name = instance.field_name()
            setattr(self, field_name, instance.value)

            if namespace not in self.object_list:
                self.object_list[namespace] = {}
            if key not in self.object_list[namespace]:
                self.object_list[namespace][key] = {}

            self.object_list[namespace][key][scope.name.upper()] = {
                "instance": instance,
                "label": key.replace("_", " ").title(),
                "key_type": key_type.value,
                "icon": ScopeIcons[scope.name.upper()].value,
            }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"all_scopes": [scope for scope in Scope]})
        context.update({"object_list": self.object_list})
        return context

    def _split_property_name(self, property_name) -> Tuple[str, str, Scope]:
        print(property_name)
        namespace, key, scope = property_name.split("__")  # type: (str,str,str)
        scope = Scope[scope.upper()]  # type:Scope
        return namespace, key, scope

    def _get_item_from_settings_key(
        self, namespace: str, key: str, scope: Scope
    ) -> "ScopedSettings":
        """Helper to get a ScopedSettings item from a property name

        Caution: if key is not present in DB, this item is created
        automatically!
        """

        from medux.settings.models import ScopedSettings

        fk = {}
        if scope == Scope.USER:
            fk["user"] = self.request.user
        elif scope == Scope.TENANT:
            # not the user's tenant, but the site's tenant!
            fk["tenant"] = self.request.tenantedsite.tenant
        # elif scope==Scope.DEVICE:
        #     fk["device"= ... ]

        item, created = ScopedSettings.objects.get_or_create(
            namespace=namespace, key=key, scope=scope, **fk
        )
        if created:
            item.save()

        return item

    def updated(self, name: str, value: str):
        # TODO: permissions checking
        # print(f"updated {name}: {value}")
        namespace, key, scope = self._split_property_name(name)
        if scope == Scope.VENDOR:
            return
        # make sure settings key is registered
        if not SettingsRegistry.exists(namespace, key, scope):
            logger.warning(f"Key {name} does not exist in registry!")
            return

        item = self._get_item_from_settings_key(namespace, key, scope)
        user = self.request.user
        # TODO: error logging
        if scope == Scope.USER and not user.has_perm("change_own_user_settings"):
            raise PermissionError(
                f"User '{user}' has no permission to change own user's settings."
            )
        if scope == Scope.TENANT and not user.has_perm("change_own_tenant_settings"):
            raise PermissionError(
                f"User '{user}' has no permission to change own tenant's settings."
            )
        if scope == Scope.GROUP and not user.has_perm("change_group_settings"):
            raise PermissionError(
                f"User '{user}' has no permission to change group settings."
            )
        # TODO: add permission checks for Device

        item.value = value
        item.save()
        messages.success(
            self.request,
            _("Successfully saved key '{key}'.").format(key=key),
        )
        logger.info(
            _("Successfully saved key '{namespace}.{key}'.").format(
                namespace=namespace, key=key
            ),
        )

    def clear(self, property_name: str):
        self.set_to(property_name, "")

    def set_active_tab(self, active_tab):
        self.active_tab = active_tab

    def toggle_field(self, property_name):
        if not property_name:
            return
        namespace, key, scope = self._split_property_name(property_name)
        if scope == Scope.VENDOR:
            return
        if not SettingsRegistry.exists(namespace, key, scope):
            return
        setattr(self, property_name, not getattr(self, property_name))

    def set_to(self, property_name, value):
        # print(property_name, value)
        if not property_name:
            return
        namespace, key, scope = self._split_property_name(property_name)
        if scope == Scope.VENDOR:
            return
        setattr(self, property_name, value)
