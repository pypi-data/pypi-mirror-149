from typing import Dict, Any

import django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms import Field
from django.views.generic.edit import FormMixin

django.setup()


class UnicornFormMixin(FormMixin):
    """Mixin for UnicornView to add Forms functionality."""

    def __init__(self, **kwargs):
        if self.success_url is not None:
            raise ImproperlyConfigured(
                f"You may not use a success URL attribute with Unicorn's {self.__class__.__name__}."
            )
        # FIXME: handle special case when "initial" is a form field -
        #  then "initial" would be the initial data of that field
        # Should we allow this? Or deny form fields named "initial"?
        if self.initial:
            raise ImproperlyConfigured(
                f"Do not use the 'initial' attr for setting initial data in a component. "
                f"Set attributes directly in the component class '{self.__class__.__name__}' instead ."
            )

        for field_name, field in self.form_class.base_fields.items():  # type: str,Field
            # set the classes Unicorn attrs dynamically, but don't override existing "initial" values
            if not hasattr(self, field_name):
                setattr(self.__class__, field_name, "")
            # This part could be improved: Should be made configureable by the user, and maybe per field?

            field.widget.attrs.update(self.get_widget_attr(field_name, field))

        super().__init__(**kwargs)

    def get_widget_attr(self, field_name: str, field: Field) -> Dict[str, Any]:
        """Returns an html attribute for the given field.

        This method can be overridden for setting special attributes to some fields. As default, it returns
        "unicorn:model"""

        if isinstance(
            field,
            (
                forms.BooleanField,
                forms.NullBooleanField,
                forms.RadioSelect,
                forms.NullBooleanSelect,
                forms.ChoiceField,
                forms.ModelChoiceField,
                forms.MultipleChoiceField,
                forms.ModelMultipleChoiceField,
                forms.TypedChoiceField,
                forms.TypedMultipleChoiceField,
            ),
        ):
            return {"unicorn:model": field_name}
        else:
            return {"unicorn:model.lazy": field_name}

    def get_initial(self):
        return self._attributes()

    # def get_context_data(self, **kwargs):
    #     """Insert the components attributes into the context dict."""
    #     kwargs.update(self._attributes())
    #     return super().get_context_data(**kwargs)

    # def get_context_data(self, **kwargs):
    #     """Insert the component's attributes into the context dict."""
    #     kwargs.update(self._attributes())
    #     return super().get_context_data(**kwargs)

    # def get_form_kwargs(self):
    #     """Return the keyword arguments for instantiating the form."""
    #     kwargs = super().get_form_kwargs()
    #     # kwargs = {
    #     #     # "initial": self.get_initial(),
    #     #     # "prefix": self.get_prefix(),
    #     # }
    #
    #     if self.request.method in ("POST", "PUT"):
    #         kwargs.update(
    #             {
    #                 "data": self.request.POST,
    #                 "files": self.request.FILES,
    #             }
    #         )
    #     return kwargs
