from django import forms
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
)
from extra_views import InlineFormSetFactory

from .forms import PrescriptionRequestForm
from .models import PrescriptionRequest, Medication
from ...core.views import TenantMixin


class MedicationInline(InlineFormSetFactory):
    model = Medication
    fields = ["name", "pkgs"]
    factory_kwargs = {
        "extra": 3,
        "widgets": {
            "name": forms.TextInput(attrs={"class": "form-control required"}),
            "pkgs": forms.TextInput(attrs={"class": "form-control"}),
        },
    }


# CreateWithInlinesView, NamedFormsetsMixin
class CreatePrescriptionRequestView(TenantMixin, CreateView):

    form_class = PrescriptionRequestForm
    success_url = reverse_lazy("thanks")
    template_name = "prescriptions/prescriptionrequest_form.html"

    def get_queryset(self):
        return PrescriptionRequest.objects.filter(tenant=self.request.tenant)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        tenant = self.request.tenant
        if tenant is None:
            self.form_invalid(form)

        # thanks to https://stackoverflow.com/a/21262262/818131
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST["tenant"] = request.tenant
        request.POST._mutable = mutable

        return super().post(request, *args, **kwargs)

    # inlines = [MedicationInline]
    # inlines_names = ["medication_inline"]


class DeletePrescriptionRequestView(DeleteView):
    model = PrescriptionRequest
    success_url = reverse_lazy("prescriptions:list")


class DeleteMedicationView(DeleteView):
    model = Medication


class PrescriptionRequestDetail(DetailView):
    model = PrescriptionRequest
