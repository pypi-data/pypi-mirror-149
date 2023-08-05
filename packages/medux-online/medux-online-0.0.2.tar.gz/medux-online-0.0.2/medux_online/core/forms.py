from typing import List

from django import forms

from medux.settings import ScopeIcons, SettingsRegistry


# from django.utils.translation import gettext_lazy as _


def snake_case_to_spaces(string):
    return string.replace("_", " ")


class PreferencesForm(forms.Form):
    """
    Dynamic form that creates fields from ScopedSettings values.
    """

    def get_context(self):
        context = super().get_context()
        fields = context["fields"]  # type: List[forms.Field]
        object_list = {}
        for field, safestr in fields:
            namespace, key, scope = field.name.split("__")
            if namespace not in object_list:
                object_list[namespace] = {}
            if key not in object_list[namespace]:
                object_list[namespace][key] = {}
            object_list[namespace][key][scope.upper()] = field

        context["object_list"] = object_list
        return context

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for namespace, key, scope, key_type in SettingsRegistry.all():
            if key_type == int:
                field = forms.IntegerField()
                field.type = "int"
            elif key_type == bool:
                field = forms.BooleanField()
                field.type = "bool"
            else:
                field = forms.CharField(max_length=255)
                field.type = "text"

            field.label = snake_case_to_spaces(key).capitalize()
            field.required = True

            # special attrs
            field.namespace = namespace
            field.scope = scope
            field.icon = ScopeIcons[scope.name.upper()]
            fieldname = "__".join(
                [
                    namespace,
                    key,
                    scope.name.lower(),
                ]
            )

            field.widget.attrs["unicorn:model.lazy"] = fieldname
            # field.widget.attrs["unicorn:error:invalid"] =\
            # "Enter a valid date/time."
            self.fields[fieldname] = field
