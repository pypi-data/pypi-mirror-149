from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Field, Column, HTML
from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from medux_online.plugins.prescriptions.models import Medication, PrescriptionRequest

MedicationFormSet = modelformset_factory(
    model=Medication,
    fields=("name", "pkgs"),
    min_num=1,
)


class PrescriptionRequestForm(forms.ModelForm):
    class Meta:
        model = PrescriptionRequest
        fields = "__all__"

    # first_name = forms.CharField(label=_("First name"))
    # last_name = forms.CharField(label=_("Last name"))
    insurance_number = forms.CharField(
        min_length=10,
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "0000TTMMYY", "class": ""}),
        label=_("Insurance number"),
    )
    # password = forms.PasswordInput()

    # medication_formset = MedicationFormSet()
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": _("e.g.: \nAmlodipin 5mg, 1 pkg,\n2x Thyrex 100 ,\n...")
            }
        ),
        label=_("Medication"),
        help_text=_(
            "Please enter the exact medication names, dosages and package counts."
        ),
    )

    helper = FormHelper()
    # helper.form_class = "form-horizontal"
    helper.layout = Layout(
        Row(
            Column(
                Field("first_name", css_class="form-control-lg"),
                css_class="col-12 col-lg-4 responsive",
            ),
            Column(
                Field("last_name", css_class="form-control-lg"),
                css_class="col-12 col-lg-4 responsive",
            ),
            Column(
                Field("insurance_number", css_class="form-control-lg"),
                css_class="col-12 col-lg-4 responsive",
            ),
        ),
        Row(
            Column(
                HTML(
                    "{%if settings.prescriptions.show_medication_message %}<div class='alert alert-warning''>"
                    "{{settings.prescriptions.medication_message}}</div>{% endif %}"
                )
            )
        ),
        Row(
            Column(
                Field("comment", css_class="form-control-lg responsive", rows="5"),
                css_class="col-12 responsive",
            ),
        ),
        FormActions(
            Submit("submit", _("Send"), css_class="btn-prescription"),
            # Submit("cancel", _("Cancel")),
        ),
    )


# TODO: delete
# class PrescriptionSettingsForm(ISettingsForm):
#     class FormSet(Form):
#         """This is the real form that is displayed in the main
#         settings page under "Prescriptions" """
#
#         prescriptions__use_requests_approval = forms.BooleanField(
#             label=Settings.get_description(
#                 "prescriptions.use_requests_approval"
#             ),
#             required=False,
#         )
#         prescriptions__show_medication_message = forms.BooleanField(
#                 label=_("Show toast at medication field"),
#                 # help_text=Settings.get_description(
#                 #     "prescriptions.show_medication_message"
#                 # ),
#                 required=False,
#         )
#
#         prescriptions__medication_message = forms.CharField(
#             label=_("Toast message"),
#             help_text=Settings.get_description(
#                 "prescriptions.medication_message"
#             ),
#             required=False,
#             widget=forms.TextInput,
#         )
#
#     def icon(self):
#         return "card-checklist"
#
#     def title(self):
#         return _("Prescriptions")
#
#     def form(self):
#         return self.FormSet
